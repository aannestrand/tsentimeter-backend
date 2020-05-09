# app.py
from flask import Flask
from pymongo import MongoClient
from twitter import store_tweets
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler
from bson import json_util 
import atexit
import json
from enum import Enum

class Months(Enum):
	JAN = 1
	FEB = 2
	MAR = 3
	APR = 4
	MAY = 5
	JUN = 6
	JUL = 7
	AUG = 8
	SEP = 9
	OCT = 10
	NOV = 11
	DEC = 12

print(Months.DEC)

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
@app.route("/api/topic/<topic>/<year>")
def tweets_topic_year(topic, year):
	# Get all tweets in a year
	tweets = db.tweets.find({"topic": topic, "date": {"$regex": ".*2020.*"}})

	# We need average sentiment of each month
	total_sentiment = 0
	total_tweets = 0
	dates = []
	for tweet in tweets:
		dates.append(tweet['date'].split()[1])
		# total_sentiment += tweet['sentiment']

	response = app.response_class(
		response=json_util.dumps(dates),
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
