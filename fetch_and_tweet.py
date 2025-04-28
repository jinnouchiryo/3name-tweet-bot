import requests
from bs4 import BeautifulSoup
import tweepy
import textwrap
import os
from datetime import datetime

# --- Twitter API認証情報 ---
API_KEY = os.environ.get("TWITTER_API_KEY")
API_SECRET = os.environ.get("TWITTER_API_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")

# --- 3name.xyz からデータ取得 ---
def fetch_ids():
    url = "https://3name.xyz/search"
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    id_elements = soup.select("div.text-2xl.font-bold.text-gray-900")
    ids = [elem.text.strip() for elem in id_elements]
    return ids

# --- Twitterに投稿 ---
def post_to_twitter(ids):
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET
    )

    today = datetime.now().strftime("%Y/%m/%d")
    header = f"【{today} 取得可能な3文字IDリスト】\n"
    message = header + ", ".join(ids)
    chunks = textwrap.wrap(message, width=270, break_long_words=False, break_on_hyphens=False)

    previous_tweet_id = None
    for chunk in chunks:
        if previous_tweet_id:
            tweet = client.create_tweet(text=chunk, in_reply_to_tweet_id=previous_tweet_id)
        else:
            tweet = client.create_tweet(text=chunk)
        previous_tweet_id = tweet.data['id']

# --- メイン実行 ---
def main():
    ids = fetch_ids()
    if ids:
        post_to_twitter(ids)
    else:
        print("IDリストが取得できませんでした。")

if __name__ == "__main__":
    main()
