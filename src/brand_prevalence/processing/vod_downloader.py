""" Twitch Video-On-Demand Downloader
"""

import os
import sys
import youtube_dl
from typing import Dict, Tuple

def download_vod(video_id: int, path_to_output_dir: str) -> Tuple[str, Dict]:
    """ Downloads a Twitch VOD referenced by its Twitch ID
        Curtesy of jaimeMF @ https://stackoverflow.com/a/18947879  
    """
    
    ydl_opts = {
        'outtmpl': os.path.join(path_to_output_dir, f'{str(video_id)}.mp4')
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(
            f"https://www.twitch.tv/videos/{video_id}",
            download = True
        )

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result
        
    return (os.path.join(path_to_output_dir, f'{str(video_id)}.mp4'), result)

if __name__ == "__main__":

    # Quick CLI Implemenation
    filename = download_vod(
        sys.argv[1], # Video ID
        sys.argv[2]  # Output Dir
    )[0]

    print(f"Finished Downloading VOD to path: {filename}")