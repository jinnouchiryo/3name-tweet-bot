import os
import requests
import tweepy
import random
import itertools

# Twitter認証
client = tweepy.Client(
    consumer_key=os.environ['TWITTER_API_KEY'],
    consumer_secret=os.environ['TWITTER_API_SECRET'],
    access_token=os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret=os.environ['TWITTER_ACCESS_SECRET']
)

# 3文字組み合わせ生成
chars = 'abcdefghijklmnopqrstuvwxyz0123456789_'
combos = itertools.product(chars, repeat=3)

# 利用可能IDリスト
available_ids = []

for combo in combos:
    username = ''.join(combo)
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url)
    
    if response.status_code == 204:  # 204 = User not found
        available_ids.append(username)

    if len(available_ids) >= 10:
        break

# 投稿する内容
if available_ids:
    tweet_text = "【空いてる3文字ID発見】\n" + "\n".join(available_ids)
else:
    tweet_text = "今日の新しい3文字IDはありませんでした！"

# ツイート送信
client.create_tweet(text=tweet_text)
print(f"ツイート完了: {tweet_text}")

