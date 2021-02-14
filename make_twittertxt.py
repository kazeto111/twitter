import tweepy
import re

#keyは実行後に削除しました
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_SECRET = ""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

path = "/Users/futo/Desktop/twitter/BarackObama1.txt"
with open(path, "a") as f:
    for tweet in tweepy.Cursor(api.user_timeline, id="BarackObama", tweet_mode='extended').items(20):
        if not tweet.entities["urls"]:#ツイート中にURLが含まれる場合は邪魔になるため削除
            f.write(re.sub("@[a-zA-Z0-9_]+", "", tweet.full_text))#ツイート中に@ooというメンションが含まれる場合は邪魔になるため削除
            f.write("\n")
            f.write("\n")
        else:
            f.write(re.sub("@[a-zA-Z0-9_]+", "", tweet.full_text.replace(tweet.entities["urls"][0]["url"], " ")))#ツイート中に@ooというメンションが含まれる場合は邪魔になるため削除
            f.write("\n")
            f.write("\n")


