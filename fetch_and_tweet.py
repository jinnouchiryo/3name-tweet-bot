import os
import requests
import tweepy
import random
import itertools
from PIL import Image, ImageDraw, ImageFont

# Twitter認証（v2用）
client = tweepy.Client(
    consumer_key=os.environ['TWITTER_API_KEY'],
    consumer_secret=os.environ['TWITTER_API_SECRET'],
    access_token=os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret=os.environ['TWITTER_ACCESS_SECRET']
)

# Twitter認証（v1.1用）←★NEW!!
auth = tweepy.OAuth1UserHandler(
    os.environ['TWITTER_API_KEY'],
    os.environ['TWITTER_API_SECRET'],
    os.environ['TWITTER_ACCESS_TOKEN'],
    os.environ['TWITTER_ACCESS_SECRET']
)
api = tweepy.API(auth)

# 3文字ID収集（以下同じ）
chars = 'abcdefghijklmnopqrstuvwxyz0123456789_'
combos = itertools.product(chars, repeat=3)

available_ids = []

for combo in random.sample(list(combos), 200):
    username = ''.join(combo)
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 204:
            available_ids.append(username)
    except:
        continue

    if len(available_ids) >= 10:
        break

# 画像生成
img_width = 800
img_height = 600
background_color = (255, 255, 255)
text_color = (0, 0, 0)

img = Image.new('RGB', (img_width, img_height), background_color)
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arial.ttf", 36)
except:
    font = ImageFont.load_default()

draw.text((30, 20), "Today's 3-Letter Available IDs", fill=text_color, font=font)

y_offset = 100
for id in available_ids:
    draw.text((30, y_offset), id, fill=text_color, font=font)
    y_offset += 50

img.save("today.png")

# 画像アップロード（v1.1のAPIで）
media = api.media_upload("today.png")

# ツイート（v2クライアントで）
client.create_tweet(text="今日の空き3文字IDリストはこちら！", media_ids=[media.media_id])

print("ツイート完了！")



