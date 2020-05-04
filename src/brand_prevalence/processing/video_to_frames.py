""" Convert a video to a series of frames using OpenCV
"""

import os
import sys
import cv2
from typing import Iterable

def to_grayscale_frames(path_to_video: str) -> Iterable:
  """ Convert a video to a series of grayscale frames using OpenCV """
  
  video_capture = cv2.VideoCapture(path_to_video)
  success, image = video_capture.read()
  while success:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    yield gray
    success, image = video_capture.read()

if __name__ == "__main__":
    """ Python -m video_to_frames.py
          path_to_video
          output_dir
    """

    # Quick CLI Implemenation
    for enum, frame in enumerate(to_grayscale_frames(sys.argv[1])):
      cv2.imwrite(os.path.join(sys.argv[2], f"{str(enum)}.jpg"))

    print(f"Finished Downloading frames to dir: {sys.argv[2]}")