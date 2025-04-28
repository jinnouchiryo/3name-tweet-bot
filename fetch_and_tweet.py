import os
import time
import tweepy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# 1. Twitter認証（v2 API用）
client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
)

# 2. Seleniumのオプション設定
chrome_options = Options()
chrome_options.add_argument('--headless')  # 画面を表示しない
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 3. ChromeDriverサービスを指定
service = Service('/snap/bin/chromium.chromedriver')

# 4. ブラウザ起動
driver = webdriver.Chrome(service=service, options=chrome_options)

# 5. laby.net/namesを開いてスクリーンショット
url = "https://laby.net/names"
driver.get(url)
time.sleep(5)  # ページ完全読み込みまで待機（秒数調整できる）
driver.save_screenshot("today.png")
driver.quit()

# 6. テキストだけツイート（無料版）
tweet_text = "今日の空き3文字IDリストはこちら！（※画像投稿は無料プラン非対応）"
client.create_tweet(text=tweet_text)

print("ツイート完了！")




