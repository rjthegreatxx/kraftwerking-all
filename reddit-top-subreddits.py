import praw
import pandas as pd
from operator import itemgetter

"""
# Reddit Trending Subreddits Script

## Steps:
1. Connect to Reddit API using PRAW.
2. Fetch top posts from the 'r/all' subreddit to identify trending subreddits.
3. Extract subreddit names, subscriber counts, URLs, and descriptions.
4. Sort subreddits in descending order based on subscriber count.
5. Adjust Pandas display settings to show all rows.
6. Convert data into a structured format (DataFrame) for display.
7. Display the most popular trending subreddits in a user-friendly table.
"""

# Reddit API Credentials
REDDIT_CLIENT_ID = 'UA7D5AALMrYUoni2QHGIow'
REDDIT_CLIENT_SECRET = '2STUrQIRC5si7RvH_2QiXcwtKdIFwQ'
REDDIT_USER_AGENT = 'python:reddit_seo_tool:1.0 (by /u/gigachadhd)'

# Initialize Reddit API
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

# Function to get trending subreddits
def get_trending_subreddits(limit=200):
    """
    Fetch trending subreddits based on top posts from 'r/all'.

    Parameters:
    limit (int): The number of posts to scan for subreddit mentions.

    Returns:
    list: A list of tuples containing subreddit names, subscriber counts, URLs, and descriptions.
    """
    trending_subs = []

    # Get top subreddits from 'r/all'
    for submission in reddit.subreddit('all').hot(limit=limit):
        subreddit_name = submission.subreddit.display_name
        subscribers = submission.subreddit.subscribers
        url = submission.subreddit.url
        description = submission.subreddit.public_description
        trending_subs.append((subreddit_name, subscribers, url, description))

    # Sort by subscriber count (descending order)
    trending_subs = sorted(trending_subs, key=itemgetter(1), reverse=True)
    return trending_subs

# Fetch trending subreddits
trending_subreddits = get_trending_subreddits()

# Adjust Pandas display settings to show all rows
pd.set_option('display.max_rows', None)

# Convert to DataFrame for display
df = pd.DataFrame(trending_subreddits, columns=['Subreddit', 'Subscribers', 'URL', 'Description'])

# Display the DataFrame
print(df)
