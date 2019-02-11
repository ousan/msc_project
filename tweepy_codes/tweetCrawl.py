import tweepy
import time
import threading
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json #data

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

trendTopicFile = open(trend_topic_file_path, "a")
tweetFile = open(tweet_file_path,"a")

TURKEY_WOE_ID = 23424969

class crawlTime():

    """ The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=10*60*60):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.timeUp=0
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            time.sleep(self.interval)
            self.timeUp=1

    def is_time_up(self):
        return self.timeUp

def get_trend_topic():
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

                ###check if tweet is valid (not a retweet)
                if tweetRT == True:
                    pass
                if tweetLang != "tr":
                    pass
                else:
                    #print("@" + username + ":" + tweet)
                    tweetFile.write("@ : " + tweetData + "\n")

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
        return


if __name__ == '__main__':
   #This handles Twitter authentification and the connection to Twitter Streaming API
    
    listener = StdOutListener()
    twitterStream = Stream(auth, listener)
    crawl_time = crawlTime()
    while crawl_time.is_time_up() != 1:
        if twitterStream.running is True:
            twitterStream.disconnect() 
            time.sleep(2)
        keywords=get_trend_topic() # return string of keywords seaprated by comma
        if keywords=='':
            print ('no keywords to listen to')
        else:
            try:
                twitterStream.filter(track=keywords,is_async=True)
            except http.client.IncompleteRead as e:
                print('client incomplete read error')
                twitterStream.disconnect()
        time.sleep(3600) # sleep for one hour and update keywords
    if twitterStream.running is True:
        twitterStream.disconnect()
        time.sleep(2)
        print("time is up")
        trendTopicFile.close()
        tweetFile.close()
 
