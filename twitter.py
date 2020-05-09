import tweepy
from pymongo import MongoClient
import requests


CONSUMER_KEY = 'HWfrcgDgiFx4sxyi8mv6fqa0I'
CONSUMER_SECRET = 'ou7mTUWUwa7n5975DBICIyvWpx4XjgGKc5iYgJqEOj8fom4y3s'
ACCESS_TOKEN = '2312617934-5AQ0ybJgdxLrXYbGU98OcSI9FavFTDuDMtAXnoh'
ACCESS_SECRET = 'E4GbLVac03Yneulpn4IGLcScrVboYtdovovytJl0kUZGu'


def connect_twitter ():
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

	api = tweepy.API(auth)
	return api

def connect_mongo ():
	client = MongoClient("mongodb+srv://ee461l-blog:trapdungeon@cluster0-1mz2k.mongodb.net/test?retryWrites=true&w=majority")
	db = client['tsentimeter']
	return db

def score_tweet(text):
	# Score all the mentions
	resp = requests.post("http://ec2-3-16-150-255.us-east-2.compute.amazonaws.com/predict", json={'data': [text]})
	scores = resp.json()
	return scores[0]


def store_tweets():
	# Connect to the Twitter API
	print("Connecting")
	api = connect_twitter()

	# Connect to the Data Base
	db = connect_mongo()
	tweets_collection = db.tweets

	# This is an example of the fields you should make in your entry
	# entry = {
	# 	'date': '',
	# 	'topic_name': '',
	# 	'search_method': '',
	# 	'tweet_id': '',
	# 	'tweet_text': '',
	# 	'num_likes': '',
	# 	'num_retweets': '',
	# 	'location': ''
	# }

	# The person or entity we are searching
	topics = ["Biden", "Trump", "ElonMusk", "CNN", "FoxNews"]

	# The type of tweet we are searching for: user_tweets, user_mentions
	search_method = "user_mentions" 

	# Our Twitter search parameters
	searchQuerys = ["@JoeBiden", "@realDonaldTrump", "@elonmusk", "@CNN", "@FoxNews"]
	retweet_filter = '-filter:retweets'
	tweetsPerQry = 15

	for i in range(0,len(searchQuerys)):

		q=searchQuerys[i]+retweet_filter

		# Get the tweets
		mentions = api.search(q=q, count=tweetsPerQry)



		# Loop throught each tweet and save an entry into database
		for mention in mentions:
				tweet = {}

				tweet['topic'] = topics[i]
				tweet['search_method'] = search_method
				tweet['date'] = mention._json['created_at']
				tweet['tweet_id'] = str(mention._json['id'])
				tweet['tweet'] = mention._json['text']
				tweet['retweet_count'] = mention.retweet_count
				tweet['favorite_count'] = mention.favorite_count

				sentiment = score_tweet(mention._json['text'])
				tweet['sentiment'] = str(sentiment)
				tweets_collection.insert_one(tweet)
				print("saved")




