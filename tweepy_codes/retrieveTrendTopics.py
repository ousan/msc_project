import sys
import tweepy
import json
 
#Authentication
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
 
# Where On Earth ID for Turkey is 23424969.
TURKEY_WOE_ID = 23424969
 
turkey_trends = api.trends_place(TURKEY_WOE_ID)
trends = json.loads(json.dumps(turkey_trends, indent=1))
 
for trend in trends[0]["trends"]:
	print("###############*******************##############")
	print (trend["name"])
	trendTweet = tweepy.Cursor(api.search, q=trend["name"]).items(2)
	for tweet in trendTweet:
		print (tweet.created_at, tweet.text)
	print("###############*******************##############\n\n")


#data = turkey_trends[0]
#trends = data['trends']

#names = [trend['name'] for trend in trends]			
#trendsName = ' \n'.join(names)
#print(len(trendsName))
#print(trendsName)


#trends = json.loads(json.dumps(turkey_trends, indent=1))
 
#for trend in trends[0]["trends"]:
#	print (trend["name"]).strip("#")
