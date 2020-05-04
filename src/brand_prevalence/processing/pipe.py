""""""

import os
import cv2
import json
import argparse

from .video_to_frames import to_frames, to_grayscale_frames
from .twitch_chat_downloader import download_twitch_chat
from .calculate_insight import timeframe_chat_activity
from .vod_downloader import download_vod
from .sift import analyze_frame

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a report over a brand logos prevalance in a given Twitch VOD")

    parser.add_argument('--video-id', type = str, required = True, dest = "video_id",
                    help="""The last segment of a Twitch VOD URL, https://www.twitch.tv/videos/589455713 would have an ID of 589455713""")

    parser.add_argument("--brand-logo", type = str, required = True, dest = "path_to_brand_logo",
                    help="Path to the branding image which prevalance you want to analyze")

    parser.add_argument("--output-dir", type = str, required = True, dest = "path_to_output_dir", 
                    help="""Path to output and working directory, 
                         files will be downloaded during analysis to this folder.""")

    parser.add_argument("--use-grayscale", dest = "use_grayscale", required = False, action = 'store_false', 
                    help="Enable conversion of frames to grayscale")

    args = parser.parse_args()
    args.video_id = int(args.video_id)
    bounding_boxes = dict()

    # Download VOD
    print(f"Downloading Twitch VOD: {args.video_id}")
    path_to_vod = download_vod(args.video_id, args.path_to_output_dir)[0]

    try:
        template = cv2.imread(args.path_to_brand_logo, cv2.IMREAD_GRAYSCALE)

        if args.use_grayscale:
            frame_generator = to_grayscale_frames
        else:
            frame_generator = to_frames

        # Start Scale Invariant Feature Detection
        print(f"Started SIFT Analysis using template: {args.path_to_brand_logo}")
        
        # Video to Frame Conversion
        for enum, frame in enumerate(frame_generator(path_to_vod)):

            print(f"Analyzing frame: {enum}")

            try:
                bounding_box = analyze_frame(frame, template)
            except KeyboardInterrupt:
                # Make script interuptable, without losing the data
                # that has been analyzed up to the point of interruption
                break
            except:
                # Naive Exception, CV2 is a mess, cannot be explicit.
                bounding_box = None

            if bounding_box != None:
                print(" - Found bounding box")
                bounding_boxes[str(enum)] = bounding_box

    except KeyboardInterrupt:
        # Make script interuptable, without losing the data
        # that has been analyzed up to the point of interruption
        pass
    print("SIFT Analysis finished, dumping file.")
    json.dump(bounding_boxes, open(os.path.join(args.path_to_output_dir, "bounding_boxes.json"), 'w'))

    # Download Twitch Chat
    print("Downloading Corrosponding Twitch Chat")
    path_to_chat_log = download_twitch_chat(args.video_id, args.path_to_output_dir)
    print("Finished Downloading Chat Log")

    # Calculate Insights
    print("Calculating Insights")
    fig = timeframe_chat_activity(path_to_chat_log, os.path.join(args.path_to_output_dir, "bounding_boxes.json"))


def run():
    return 0