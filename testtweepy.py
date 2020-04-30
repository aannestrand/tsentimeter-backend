import tweepy
from pymongo import MongoClient

CONSUMER_KEY = 'HWfrcgDgiFx4sxyi8mv6fqa0I'
CONSUMER_SECRET = 'ou7mTUWUwa7n5975DBICIyvWpx4XjgGKc5iYgJqEOj8fom4y3s'
ACCESS_TOKEN = '2312617934-5AQ0ybJgdxLrXYbGU98OcSI9FavFTDuDMtAXnoh'
ACCESS_SECRET = 'E4GbLVac03Yneulpn4IGLcScrVboYtdovovytJl0kUZGu'

# def connect_twitter ():
# 	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# 	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# 	api = tweepy.API(auth)
# 	return api

# api = connect_twitter()

# # The person or entity we are searching
# topics = ["Trump"]

# # The type of tweet we are searching for: user_tweets, user_mentions
# search_method = "user_mentions" 

# # Our Twitter search parameters
# searchQuerys = "realDonaldTrump"
# retweet_filter = '-filter:retweets'
# tweetsPerQry = 1
# q=searchQuerys+retweet_filter

# # Get the tweets
# mentions = api.search(q=q, count=tweetsPerQry)

# for mention in mentions:
#     print(mention._json['id'])
#     print(mention._json['text'])

def connect_mongo ():
	client = MongoClient("mongodb+srv://ee461l-blog:trapdungeon@cluster0-1mz2k.mongodb.net/test?retryWrites=true&w=majority")
	db = client['tsentimeter']
	return db


# Connect to the Data Base
db = connect_mongo()
tweets_collection = db.tweets

tweets = tweets_collection.find()

for tweet in tweets:
    tweet['tweet_id'] = str(tweet['tweet_id'])
    tweets_collection.save(tweet)
    print("Success")