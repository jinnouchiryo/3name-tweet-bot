import os
import time
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tweepy

# 環境変数からTwitter APIキーを取得
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET = os.environ['TWITTER_API_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

# セレニウム設定
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

# サイトを開く
driver.get('https://laby.net/names')
time.sleep(5)  # ページ読み込み待機

# スクリーンショット保存
screenshot_path = 'today.png'
driver.save_screenshot(screenshot_path)
driver.quit()

# 画像からIDリスト部分を切り抜き
full_img = Image.open(screenshot_path)

# ここは適宜調整！（今は仮の座標）
# 【左, 上, 右, 下】で範囲指定（px単位）
cropped_img = full_img.crop((50, 200, 600, 800))  
cropped_path = 'cropped_today.png'
cropped_img.save(cropped_path)

# OCRで画像から文字読み取り
text = pytesseract.image_to_string(Image.open(cropped_path), lang='eng')

# 投稿する本文作成
tweet_text = f"今日の空き3文字IDリストはこちら！\n\n{text.strip()}"

# Twitterに投稿
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
)
api = tweepy.API(auth)

api.update_status(status=tweet_text)

print("投稿完了！")





