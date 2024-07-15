from utils.constants import CLIENT_ID, SECRET_KEY, OUTPUT_PATH
from etls.reddit_etl import connect_reddit, extract_posts, transform_data, load_data_to_csv
import pandas as pd


def reddit_pipeline(file_name: str, subreddit: str, time_filter: str = "day", limit: int | None = None):
    # Connect to Reddit Instance
    instance = connect_reddit(CLIENT_ID, SECRET_KEY, "Airscholar Agent")

    # Extraction
    posts = extract_posts(instance, subreddit, time_filter, limit)

    # Transformation
    posts_df: pd.DataFrame = transform_data(posts)

    # Load to csv
    file_path = f"{OUTPUT_PATH}/{file_name}.csv"
    load_data_to_csv(posts_df, file_path)
    
    return file_path
