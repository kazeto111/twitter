from time import sleep
import schedule
from requests_oauthlib import OAuth1Session
import tweepy
import re
import csv
import pprint

#スクレイピング用の関数定義
def tweet_scrapping():
  CK = ""
  CS = ""
  AT= ""
  AS= ""
  auth = tweepy.OAuthHandler(CK, CS)
  auth.set_access_token(AT, AS)
  api = tweepy.API(auth)
  Cursor = tweepy.Cursor(api.user_timeline).items() #自分のツイートを取得
  tweet_list = []
  with open("my_twitter.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
      tweet_list.append(row)

  tweet_list_t = [list (i) for i in zip (*tweet_list)]
  tweet_id_list = tweet_list_t[3]

  p = re.compile('[a-z]') #英語を含むツイートのみを取得
  with open("my_twitter.csv", "a") as f:
    writer = csv.writer(f)
    for status in Cursor:
      try:
          text = str(status.text).replace("\n","")    # ツイート内の改行を削除
          if p.search(text): #英語を含むツイートのみを取得
            if status.id in tweet_id_list:
              pass
            elif "RT" in text:  # RTは書き込まない
              pass
            elif "https" in text: # 画像つきとURL付きツイートを書き込まない
              pass
            elif "@" in text: # リプの場合は書き込まない
              pass
            else:
              writer.writerow(text)
      except UnicodeEncodeError: # 実行していると突然UnicodeEncodeErrorが出るが続ける
          pass

update_url = "https://api.twitter.com/1.1/statuses/update.json"
#ツイート用の関数定義
def tweet(flag = [1]): #flagリストは全く同じツイートを続けて行うとtweitter apiにブロックされてしまうため各ツイートに番号をつけることで
  #文章を全く同じではないようにしブロックされるのを回避するため
  CK = "" 
  CS = ""
  AT= ""
  AS= ""
  twitter = OAuth1Session(CK, CS, AT, AS)
  with open("/content/drive/My Drive/機械学習/bert_generatetion/predict.txt", "r") as f:
    s = f.read()
  s = "tweet like obama No" + str(flag[0]) + "\n" + s #ツイートに番号をつける
  print(s)
  body = s
  flag[0] = flag[0] + 1
  params = {"status" : body}
  res = twitter.post(update_url, params = params)
  if res.status_code == 200:
    print("Success")
  else:
    print("code : %d"% res.status_code)


schedule.every(10).minutes.do(tweet_scrapping)
schedule.every(3).minutes.do(tweet)
while True:
  schedule.run_pending()
  sleep(1)
