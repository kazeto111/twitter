from time import sleep
import schedule
from requests_oauthlib import OAuth1Session
import tweepy
import re
import csv
import pprint
import pandas as pd

def tweet_scrapping():
    CK = ""
    CS = ""
    AT = ""
    AS = ""
    # keyは見せられないため消しました
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)
    Cursor = tweepy.Cursor(api.user_timeline).items(50)
    tweet_df = pd.read_csv("my_twitter.csv", header=None)


    p = re.compile('[a-z]')
    for status in Cursor:
        # print()
        try:
            text = str(status.text).replace("\n", "")  # ツイート内の改行を削除
            # print(text)
            if p.search(text):  # 英語のツイートしか書き込まない
                if status.id in tweet_df.iloc[:,3]:
                    print("a")
                    tweet_df[tweet_df.index.get_loc(str(status.id)), 1] = status.favorite_count
                    pass
                elif "RT" in text:  # RTは書き込まない
                    pass
                elif "https" in text:  # 画像つきとURL付きツイートを書き込まない
                    pass
                elif "@" in text:  # リプの場合は書き込まない
                    pass
                else:
                    one_tweet_list = [text, status.favorite_count, status.retweet_count, status.id]
                    tweet_df.append(one_tweet_list)
        except UnicodeEncodeError:  # 実行していると突然UnicodeEncodeErrorが出るが続ける
            pass
    tweet_df.to_csv("my_twitter.csv", header=False, index=False)
    print(tweet_df)

