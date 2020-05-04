""" Calculate Insightful statistics and 
    receive plotted and readable extracts.
    
"""
import sys
import json
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

def _to_seconds(timestamp: str) -> int:
    """ Converts a string timestamp of format
        [hours:minutes:seconds] to seconds
    """
    
    # Hours to seconds
    seconds = int(timestamp.split('[')[1].split(':')[0]) * 60 * 60 

    # Minutes to seconds
    seconds += int(timestamp.split(':')[1].split(':')[0]) * 60

    # Add seconds
    seconds += int(timestamp.split(':')[-1][:-1])

    return seconds

def _make_unique(path_to_chat_log: str, UNIQUENESS: int = 10) -> Dict:

    UNIQUE_TIME_BETWEEN_POSTS = 10 # Seconds
    USER_POST_TRACKER = defaultdict(int)
    POSTS = defaultdict(int)

    for enum, post in enumerate(open(path_to_chat_log, 'r', encoding="utf8").read().split('\n')[:500]):
        post = post.split(' ')
        if not len(post) >= 2:
            continue

        timestamp, username = post[0], post[1]
        timestamp = _to_seconds(timestamp)

        # If the user had a comment counted within a certain time
        # since the current comment was posted, ignore it.
        if abs(timestamp - USER_POST_TRACKER[username]) <= UNIQUE_TIME_BETWEEN_POSTS:
            print(f'Ignoring comment number: {enum} from user "{username}"')
            continue
        
        # Otherwise, count it and update the timestamp.
        else:
            USER_POST_TRACKER[username] = timestamp
            POSTS[str(timestamp)] += 1

    return POSTS

def exposure_as_percent_of_video(path_to_bounding_boxes: str, video_lenght_in_seconds: int, fps: int = 60) -> float:
    """ Returns what percentage of a videos lenght
        the given logo was visible in.
    """
    
    # Load bounding boxes
    boxes = json.load(open(path_to_bounding_boxes, 'r', encoding='utf8'))

    # Calculate Percentage
    percent = ((1 / fps) * len(boxes.keys())) / video_lenght_in_seconds * 100

    print(f"the timeframes in bounding_boxes.json make up {percent}% of the total video")

    return percent

def percent_of_chat_activiy(path_to_chat_log: str, timeframes: List[Tuple[int]]) -> float:
    """ Returns the total percentage of chat activity
        experienced during the given timeframes
    """ 

    POSTS = _make_unique(path_to_chat_log, 10)
    total_posts = sum(POSTS.values())

    print(f"There is a total of {total_posts} comments in the given chat log")

    timeframe_posts = list()
    for enum, timeframe in enumerate(timeframes):
        posts_during_timeframe = sum([POSTS[str(timestamp)] for timestamp in timeframe])
        percent = posts_during_timeframe / total_posts * 100
        timeframe_posts.append(posts_during_timeframe)
        print(f"""timeframe: {timeframe}, saw a total of {posts_during_timeframe} posts, which is {percent}% of the total chat activity""")

    collective_percentage = sum(timeframe_posts) / total_posts * 100 
    print(f"Collectively, the timeframes got {collective_percentage}% of the chat activity")
    return collective_percentage

def timeframe_chat_activity(path_to_chat_log: str, path_to_bounding_boxes: str):
    """ Creates a matplotlib plot showing the chat activity
        and the timeframes of branding exposure together.
    """

    posts = _make_unique(path_to_chat_log, 10)
    fig, ax = plt.subplots()

    ax.plot(list(posts.keys()), list(posts.values()) , '.r-')

    # Plot timeframes in which bounding boxes are visible
    for key in list(json.load(open(path_to_bounding_boxes, 'r')).keys()):
        ax.plot(int(key) / 60, max(list(posts.values())) + 1 , '_b-',)

    plt.title("Chat Activity and Logo Visibility")
    plt.xlabel("Seconds into the video")
    plt.xticks(fontsize=8, rotation=65)
    plt.ylabel("Number of comments made at timestep")

    return plt
