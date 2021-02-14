from time import sleep
import schedule
from requests_oauthlib import OAuth1Session
CK = ""
CS = ""
AT = ""
AS = ""
update_url = "https://api.twitter.com/1.1/statuses/update.json"
def tweet():
  twitter = OAuth1Session(CK, CS, AT, AS)
  body = "mymymytweet!"
  params = {"status" : body}
  res = twitter.post(update_url, params = params)
  if res.status_code == 200:
    print("Success")
  else:
    print("code : %d"% res.status_code)

def job():
  # 定期実行させたい処理
  print('Do Action')


if __name__ == "__main__":
  #schedule.every().day.at("01:40").do(tweet)
  schedule.every(1).minutes.do(tweet)
  schedule.every(1).minutes.do(job)
  tweet()
  while True:
    schedule.run_pending()
    sleep(1)
