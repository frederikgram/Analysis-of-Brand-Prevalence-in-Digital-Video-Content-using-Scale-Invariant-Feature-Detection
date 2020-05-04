""" """

import numpy as np
import sys
import cv2 as cv
import cv2 as cv2
import os
import json
import matplotlib.pyplot as plt


def analyze_frame(frame, template):
    img1 = template
    img2 = frame

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in range(len(matches))]

    j = 0
    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1,0]
            j += 1

    if j < 20:
        dontDraw = True
    else:
        dontDraw = False

    draw_params = dict(matchColor = (0,255,0),
                    matchesMask = matchesMask,
                    flags = cv.DrawMatchesFlags_DEFAULT)
    #img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

    #--------#
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1,des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)

    good_matches = matches[:10]
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches     ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h,w = img1.shape[:2]
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

    dst = cv2.perspectiveTransform(pts,M)
    dst += (w, 0)  # adding offset

    if not dontDraw:
        return [str(dst[0]), str(dst[1]), str(dst[2]), str(dst[3])]
    else:
        return None

if __name__ == "__main__":
    
    frame = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)

    # Quick CLI Compatible Implemenation
    bounding_box = analyze_frame(
        frame,
        template
    )

    if bounding_box == None:
        print("No bounding boxes were found that matched the template")
    else:
        print(f"A bounding box was found at location: {bounding_box}")
