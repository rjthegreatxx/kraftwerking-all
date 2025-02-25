import praw
import requests
import re
from collections import Counter
import pandas as pd

"""
# Reddit & Ahrefs Keyword Research Script

## Steps:
1. Scrape top posts from selected subreddits: 
   - "dataengineering"
   - "webdev"
   - "sysadmin"
   - "marketing"

2. Extract the most frequently mentioned keywords from post titles.

3. Query Ahrefs API to check:
   - Search Volume
   - Keyword Difficulty (KD)
   - Cost-Per-Click (CPC)

4. Display a table with the most promising keywords based on:
   - High Search Volume
   - Low Keyword Difficulty (Easier to rank)
   - High CPC (Indicates commercial intent)

"""

# Reddit API Credentials (Set these up at https://www.reddit.com/prefs/apps)
REDDIT_CLIENT_ID = 'UA7D5AALMrYUoni2QHGIow'
REDDIT_CLIENT_SECRET = '2STUrQIRC5si7RvH_2QiXcwtKdIFwQ'
REDDIT_USER_AGENT = '"python:reddit_seo_tool:1.0 (by /u/gigachadhd)"'

# Ahrefs API Key (or use Google Keyword Planner if Ahrefs is unavailable)
AHREFS_API_KEY = 'your_ahrefs_api_key'

# Initialize Reddit API
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

# Function to get trending subreddit posts
def get_trending_keywords(subreddit_name, post_limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    titles = [post.title for post in subreddit.hot(limit=post_limit)]
    
    words = []
    for title in titles:
        words.extend(re.findall(r'\b\w+\b', title.lower()))
    
    common_words = Counter(words).most_common(20)
    return common_words

# Function to check keyword difficulty and search volume using Ahrefs
def check_keyword_in_ahrefs(keyword):
    api_url = f"https://api.ahrefs.com/v3/keywords-explorer?token={AHREFS_API_KEY}&keywords={keyword}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if 'keywords' in data and len(data['keywords']) > 0:
            keyword_data = data['keywords'][0]
            return {
                'Keyword': keyword,
                'Search Volume': keyword_data.get('search_volume', 'N/A'),
                'Keyword Difficulty': keyword_data.get('keyword_difficulty', 'N/A'),
                'CPC': keyword_data.get('cpc', 'N/A')
            }
    return {'Keyword': keyword, 'Search Volume': 'N/A', 'Keyword Difficulty': 'N/A', 'CPC': 'N/A'}

# Define subreddits to analyze
subreddits = ["dataengineering", "webdev", "sysadmin", "marketing"]

# Extract trending keywords from each subreddit
keyword_results = []
for subreddit in subreddits:
    trending_keywords = get_trending_keywords(subreddit)
    for keyword, count in trending_keywords:
        keyword_data = check_keyword_in_ahrefs(keyword)
        keyword_results.append(keyword_data)

# Convert to DataFrame and display
df = pd.DataFrame(keyword_results)
import ace_tools as tools
tools.display_dataframe_to_user(name="Keyword Research Results", dataframe=df)
