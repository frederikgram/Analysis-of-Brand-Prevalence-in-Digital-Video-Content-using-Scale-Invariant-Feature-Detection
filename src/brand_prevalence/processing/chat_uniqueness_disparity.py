""" Calculate the number of unique chat posts
    using different uniqueness-heuristics
    
"""
import sys
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

from .calculate_insight import _to_seconds
from collections import defaultdict

def uniqueness(path_to_chat_log: str):
    """ Returns a plot depicting
        the number of unique posts, given
        different requirements for uniqueness
    """

    x,y = list(), list()

    for UNIQUENESS_HEURISTIC in range(0, 60):

        USER_POST_TRACKER = defaultdict(int)
        total_posts = 0

        for post in open(path_to_chat_log, 'r', encoding="utf8").read().split('\n'):
            
            post = post.split(' ')
            if not len(post) >= 2:
                continue

            timestamp, username = post[0], post[1]
            timestamp = _to_seconds(timestamp)

            if abs(timestamp - USER_POST_TRACKER[username]) <= UNIQUENESS_HEURISTIC:
                continue
            else:
                USER_POST_TRACKER[username] = timestamp
                total_posts += 1

        x.append(UNIQUENESS_HEURISTIC)
        y.append(total_posts)

    plt.plot(x, y)
    plt.title("Post Volume by Uniqueness Heuristic")
    plt.xlabel("Minimum Time(s) Between Posts")
    plt.ylabel("Number of Unique Posts")

    return plt

if __name__ == "__main__":
    
    # Quick CLI Implemenation
    plt = uniqueness(
        sys.argv[1], # path_to_chat_log
    )

    plt.show()
