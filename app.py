# app.py
from flask import Flask, jsonify
from pymongo import MongoClient
from twitter import store_tweets
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler
from bson import json_util 
import atexit
import json
from enum import Enum
from collections import defaultdict, OrderedDict

# Define our app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to our database
client = MongoClient("mongodb+srv://ee461l-blog:trapdungeon@cluster0-1mz2k.mongodb.net/test?retryWrites=true&w=majority")
db = client['tsentimeter']

# This is our cron job for getting tweets
scheduler = BackgroundScheduler()
scheduler.add_job(func=store_tweets, trigger="interval", minutes=15)
scheduler.start()

# Shutdown cronjob if process is stopped
atexit.register(lambda: scheduler.shutdown(wait=False))


@app.route("/api")
def hello():
    return "Hello World!"


# This end point returns monthly sentiments for the year
@app.route("/api/topic/<topic>/date/<year>")
def tweets_topic_year(topic, year):
	# Get all tweets in a year
	tweets = db.tweets.find({"topic": topic, "date": {"$regex": ".*{}.*".format(year)}})

	# We need total sentiment of each month
	total_sentiment = defaultdict(int)
	total_tweets = defaultdict(int)
	for tweet in tweets:
		total_sentiment[tweet['date'].split()[1]] += float(tweet['sentiment'])
		total_tweets[tweet['date'].split()[1]] += 1

	# Now we can get the average
	for month in total_sentiment.keys():
		total_sentiment[month] /= total_tweets[month]

	# 
	sentiments = []
	for month in total_sentiment.keys():
		arr = {"month": month, "sentiment": total_sentiment[month], "total_tweets": total_tweets[month]}
		sentiments.append(arr)

	final = {"sentiments": sentiments}
	return jsonify(final)


# This end point returns the daily sentiment in a month
@app.route("/api/topic/<topic>/date/<year>/<month>")
def tweets_topic_month(topic, year, month):
	# Get all tweets in a year and month
	tweets = db.tweets.find({"topic": topic, "date": {"$regex": ".*{}.*".format(year), "$regex": ".*{}.*".format(month)}})

	# We need the total sentiment for each day
	total_sentiment = defaultdict(int)
	total_tweets = defaultdict(int)
	for tweet in tweets:
		total_sentiment[tweet['date'].split()[2]] += float(tweet['sentiment'])
		total_tweets[tweet['date'].split()[2]] += 1

	# Now we can get the average
	for day in total_sentiment.keys():
		total_sentiment[day] /= total_tweets[day]

	response = app.response_class(
		response=json_util.dumps({'sentiment': total_sentiment, 'tweets': total_tweets}),
		status=200
    )
	return response


# This end point returns the hourly sentiment in a day
@app.route("/api/topic/<topic>/date/<year>/<month>/<day>")
def tweets_topic_day(topic, year, month, day):
	# Get all tweets in a year and month
	tweets = db.tweets.find({"topic": topic, "date": {"$regex": ".*{}.*".format(year), "$regex": ".*{}.*".format(month), "$regex": ".*{}.*".format(day)}})

	# We need the total sentiment for each hour
	total_sentiment = defaultdict(int)
	total_tweets = defaultdict(int)
	for tweet in tweets:
		total_sentiment[tweet['date'].split()[3].split(":")[0]] += float(tweet['sentiment'])
		total_tweets[tweet['date'].split()[3].split(":")[0]] += 1

	# Now we can get the average
	for hour in total_sentiment.keys():
		total_sentiment[hour] /= total_tweets[hour]

	total_tweets = OrderedDict(sorted(total_tweets.items()))
	total_sentiment = OrderedDict(sorted(total_sentiment.items()))

	response = app.response_class(
		response=json_util.dumps({'sentiment': total_sentiment, 'tweets': total_tweets}),
		status=200
    )
	return response	


# This end point returns count amount of tweets for a given topic and sentiment
@app.route("/api/topic/<topic>/sentiment/<sentiment>/<count>")
def tweets_topic_sentiment_count(topic, sentiment, count):

	# If the desired sentiment is positive
	if (sentiment == "1"):
		tweets = db.tweets.find({"topic": topic, "sentiment": {"$gte": "0.8"}}).limit(int(count))
	
	# If the desired sentiment is negative
	else:
		tweets = db.tweets.find({"topic": topic, "sentiment": {"$lte": "0.2"}}).limit(int(count))

	tweet_ids = []
	for tweet in tweets:
		tweet_ids.append(tweet['tweet_id'])

	response = app.response_class(
		response=json_util.dumps({'tweet_ids': tweet_ids}),
		status=200
    )
	return response	


# This end point returns all tweets for a given topic
@app.route("/api/tweets/topic/<topic>")
def tweets_topic(topic):
    tweets = db.tweets.find({"topic": topic})

    response = app.response_class(
        response=json_util.dumps(tweets[0]),
        status=200
    )

    return response

if __name__ == '__main__':
    app.run(debug=True)
