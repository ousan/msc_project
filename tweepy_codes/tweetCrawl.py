import tweepy
import time
import threading
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json #data
import re
from urllib3.exceptions import ProtocolError

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

tweetFile = open(tweet_file_path,"a")
TURKEY_WOE_ID = 23424969

def get_trend_topic():
    trendTopicFile = open(trend_topic_file_path, "a")
    counter = 0
    trend_topics = []
    turkey_trends = api.trends_place(TURKEY_WOE_ID)
    trends = json.loads(json.dumps(turkey_trends, indent=1))
    for trend in trends[0]["trends"]:
        counter = counter + 1 
        trend_topics.append(str(trend["name"]))
        trendTopicFile.write("%s\n" % trend["name"])
        if counter >= 10:
            break
        #print(trend["name"])
    trendTopicFile.write("\n")    
    trendTopicFile.close()
    return trend_topics

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self):
        self.prevTime = 0

    def on_data(self, data):
        #start_time = time.time()
        #elapsed_time = time.time() - self.prevTime
        #self.prevTime = time.time()
        #print(elapsed_time)
        try:
            tweet = json.loads(data.strip())
            if 'text' in tweet and 'lang' in tweet and 'retweeted' in tweet: 
                tweetData = tweet["text"]
                tweetLang = tweet["lang"]
                tweetRT = tweet["retweeted"]

                if tweetRT == True: #check if tweet is valid (not a retweet)
                    return
                if tweetLang != "tr": #check if tweet language is valid
                    return
                else:
                    tweetData=tweetData.replace("\n"," ")
                    tweetFile.write(tweetData + "\n")

        except tweepy.TweepError as e:
            print(e.reason)
            #ime.sleep(5)

        #elapsed_time = time.time() - start_time
        #print("elapsed_time")
        #print(elapsed_time)

    def on_error(self, status):
        #error number 503, servers down
        print ('Error #:', status)

    def on_exception(self,exception):

        print("EXCEPTION OCCURED!!!!\n")
        print(exception)
        


if __name__ == '__main__':
   #This handles Twitter authentification and the connection to Twitter Streaming API
    listener = StdOutListener()
    twitterStream = Stream(auth, listener)
    
    try:
        while True:

            if twitterStream.running is True:
                print("Stream is closing to renew ttList")
                twitterStream.disconnect() 
                time.sleep(2)
            
            keywords=get_trend_topic() # return string of keywords seaprated by comma        
            if keywords=='':
                print ('no keywords to listen to')
            else:
                twitterStream.filter(track=keywords,is_async=True)
            time.sleep(60*60) # sleep for one hour and update keywords

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        tweetFile.close()
        if twitterStream.running is True:
            twitterStream.disconnect() 
        
