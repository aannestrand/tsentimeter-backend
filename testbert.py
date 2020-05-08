from pymongo import MongoClient
import requests
import json


def connect_mongo ():
	client = MongoClient("mongodb+srv://ee461l-blog:trapdungeon@cluster0-1mz2k.mongodb.net/test?retryWrites=true&w=majority")
	db = client['tsentimeter']
	return db

def score_database():
	tweets_collection = connect_mongo().tweets
	all_tweets = tweets_collection.find({"sentiment": {"$exists": False}})

	batch_size = 10
	tweet_number = 0
	batch_objects = []
	batch_tweets = []

	for tweet in all_tweets:
		batch_objects.append(tweet)
		batch_tweets.append(tweet['tweet'])
		tweet_number += 1

		if (tweet_number % batch_size == 0):
			resp = requests.post("http://ec2-3-16-150-255.us-east-2.compute.amazonaws.com/predict", json={'data': batch_tweets})
			scores = resp.json()

			for i in range(0, len(scores)):
				tweets_collection.update_one({"_id": batch_objects[i]["_id"]}, {"$set": {"sentiment": scores[i]}})

			batch_objects.clear()
			batch_tweets.clear()


if __name__ == '__main__':
	score_database()