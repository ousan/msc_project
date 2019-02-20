import tweepy
import time
import threading
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json #data
import re
from urllib3.exceptions import ProtocolError
import datetime

################################ Variables ####################################
#Storage Path
trend_topic_file_path = "/home/oguzhaner/Desktop/ttFile" 
tweet_file_path = "/home/oguzhaner/Desktop/tweetFile" 

#Authentication
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

#Trend Topic Country
TURKEY_WOE_ID = 23424969

#TT Update Time
hour=1
minute=0
second=0

#Config
timeStampEnabled=True
usernameEnabled=True
################################################################################
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweetFile = open(tweet_file_path,"a")

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
            #print (tweet)
            if 'text' in tweet and 'lang' in tweet and 'retweeted' in tweet and 'user' in tweet: 
                tweetData = tweet["text"]
                tweetLang = tweet["lang"]
                tweetExtension ="" # this is used to add username and timestamp if it is wanted
                
                if tweet['retweeted'] or "RT @" in tweet['text']: #including 'unofficial' re-tweets, you should check the string for the substring 'RT @'
                    return
                if tweetLang != "tr": #check if tweet language is valid
                    return

                if timeStampEnabled == True:
                    tweetExtension = datetime.datetime.now().strftime("%d. %B %Y %I:%M%p ") 
                if usernameEnabled == True:
                    tweetExtension = tweetExtension + "@" + tweet["user"]["screen_name"]
                if usernameEnabled == True or timeStampEnabled == True:
                    tweetExtension = tweetExtension + " => "

                tweetData = tweetExtension + tweetData
                tweetData=tweetData.replace("\n"," ")
                #print(tweetData)
                tweetFile.write(tweetData + "\n")

        except tweepy.TweepError as e:
            print(e.reason)

        #elapsed_time = time.time() - start_time
        #print("elapsed_time")
        #print(elapsed_time)

    def on_error(self, status):
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
            
            keywords=get_trend_topic() # return string of keywords seperated by comma        
            if keywords=='':
                print ('no keywords to listen to')
            else:
                twitterStream.filter(track=keywords,is_async=True)
            time.sleep((hour*3600) + (minute*60) + (second))

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        tweetFile.close()
        if twitterStream.running is True:
            twitterStream.disconnect() 
        
