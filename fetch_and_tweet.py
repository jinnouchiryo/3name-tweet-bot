import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tweepy

# Twitter API keys from GitHub Secrets
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

# 1. ヘッドレスChrome設定
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 2. ブラウザ起動
driver = webdriver.Chrome(options=chrome_options)

# 3. ページを開く
url = "https://laby.net/names"
driver.get(url)
time.sleep(5)  # ページ完全読み込み待機（必要に応じて秒数調整）

# 4. スクリーンショット保存
driver.save_screenshot("today.png")

# 5. ブラウザ閉じる
driver.quit()

# 6. Twitter認証
auth = tweepy.OAuth1UserHandler(
    API_KEY, API_SECRET,
    ACCESS_TOKEN, ACCESS_SECRET
)
api = tweepy.API(auth)

# 7. ツイート＋画像アップロード
tweet_text = "今日の空き3文字IDリストはこちら！"
media = api.media_upload("today.png")
api.update_status(status=tweet_text, media_ids=[media.media_id])

print("ツイート完了！")



