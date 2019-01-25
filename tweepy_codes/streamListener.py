import tweepy
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json #data

#Authentication
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

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

            print ("@" + username + ": " + tweet + "")
            #print ("followers = " + str(followers))
    

if __name__ == '__main__':
   #This handles Twitter authentification and the connection to Twitter Streaming API
    l = StdOutListener()
    stream = Stream(auth, l)

    #This line filters Twitter Streams to capture data by keyword
    stream.filter(track=['ankara'])
