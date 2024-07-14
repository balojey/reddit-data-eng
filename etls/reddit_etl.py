from praw import Reddit
from utils.constants import POST_FIELDS
import pandas as pd
import numpy as np


def connect_reddit(client_id, secret_key, user_agent) -> Reddit:
    try:
        reddit = Reddit(
            client_id=client_id,
            client_secret=secret_key,
            user_agent=user_agent
        )
        print("Connected to reddit")
        return reddit
    except Exception as e:
        print(e)
        sys.exit(1)


def extract_posts(instance: Reddit, subreddit: str, time_filter: str, limit: str | None = None) -> list:
    subreddit = instance.subreddit(subreddit)
    posts = subreddit.top(time_filter=time_filter, limit=limit)
    
    posts_list = []
    
    for post in posts:
        post_dict = vars(post)
        post = {key: post_dict[key] for key in POST_FIELDS}
        print(post)
        posts_list.append(post)

    return posts_list


def transform_data(posts: list) -> pd.DataFrame:
    posts_df = pd.DataFrame(posts)
    posts_df["created_utc"] = pd.to_datetime(posts_df["created_utc"], unit="s")
    posts_df["over_18"] = np.where((posts_df["over_18"] == True), True, False)
    posts_df["author"] = posts_df["author"].astype(str)
    edited_mode = posts_df["edited"].mode()
    posts_df["edited"] = np.where((posts_df["edited"].isin([True, False])), posts_df["edited"], edited_mode).astype(bool)
    posts_df["num_comments"] = posts_df["num_comments"].astype(int)
    posts_df["score"] = posts_df["score"].astype(int)
    posts_df["upvote_ratio"] = posts_df["upvote_ratio"].astype(int)
    posts_df["selftext"] = posts_df["selftext"].astype(str)
    posts_df["title"] = posts_df["title"].astype(str)
    return posts_df


def load_data_to_csv(data: pd.DataFrame, path: str):
    data.to_csv(path, index=False)
