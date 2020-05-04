""" Simple interface to use
    PetterKraabol's Twitch-Chat-Downloader
    
    # https://github.com/PetterKraabol/Twitch-Chat-Downloader
"""

import os
import sys
import subprocess

def download_twitch_chat(video_id: int, path_to_output_dir: str, twitch_id: str) -> str:
    """ Downloads the given Twitch VODs
        chat as irc format
    """
    
    # Start subprocess
    p = subprocess.Popen([
        "tcd", "--video", str(video_id),
        "--format", "irc",
        "--output", path_to_output_dir,
        "--client-id", twitch_id],
        shell=True)

    # Wait for subprocess to finish
    p_status = p.wait()

    return os.path.join(path_to_output_dir, f"{str(video_id)}.log")

if __name__ == "__main__":
    
    # Quick CLI Implemenation
    filename = download_twitch_chat(
        sys.argv[1], # Video ID
        sys.argv[2], # Output Dir
        sys.argv[3]  # Twitch ID
    )

    print(f"Finished Downloading Chat log of VOD {sys.argv[1]} to path: {filename}")