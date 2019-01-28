import tweepy
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json #data
import datetime

#Storage Path
trend_topic_file_path = "/home/oguzhaner/Desktop/ttFile" 
tweet_file_path = "/home/oguzhaner/Desktop/tweetFile" 

#Authentication
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

trendTopicFile = open(trend_topic_file_path, "a")
tweetFile = open(tweet_file_path, "a")

TURKEY_WOE_ID = 23424969
def getTrendTopic():
    trend_topics = []
    turkey_trends = api.trends_place(TURKEY_WOE_ID)
    trends = json.loads(json.dumps(turkey_trends, indent=1))
    for trend in trends[0]["trends"]:
        trend_topics.append(str(trend["name"]))
        trendTopicFile.write("%s\n" % trend["name"])
        print(trend["name"])
    return trend_topics

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            jsonData = json.loads(data.strip())
            tweetID = jsonData.get("id_str")
            tweetData = api.get_status(tweetID)

            #check if tweet is valid (not a retweet)
            self.check_valid_tweet(tweetData)

        except (tweepy.error.RateLimitError):
            print ("This is the error I'm receiving")
            time.sleep(60*15)

    def on_error(self, status):
        #error number 503, servers down
        print ('Error #:', status)

    def check_valid_tweet(self, tweetData):
        #Check if data is the original tweet or a retweet
        if ( (hasattr(tweetData, 'retweeted_status')) ):
            pass
        else:
            tweet = tweetData.text
            username = tweetData.author.screen_name
            followers = tweetData.author.followers_count
            with open(tweet_file_path,'a') as tf:
                tf.write("@" + username + ": " + tweet + "\n")
            print("@" + username + ": " + tweet + "")
            #print ("followers = " + str(followers))
    

if __name__ == '__main__':
   #This handles Twitter authentification and the connection to Twitter Streaming API
    listener = StdOutListener()
    twitterStream = Stream(auth, listener)
    keywords = getTrendTopic()
    print(type(keywords))
    while True:
        if twitterStream.running is True:
            twitterStream.disconnect() 
        keywords=getTrendTopic() # return string of keywords seaprated by comma
        if keywords=='':
            print ('no keywords to listen to')
        else:
            twitterStream.filter(languages=["tr"],track=keywords,is_async=True) # Open the stream to work on asynchronously on a different thread
        time.sleep(3600) # sleep for one hour
