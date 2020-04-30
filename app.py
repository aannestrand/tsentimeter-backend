# app.py
from flask import Flask
from pymongo import MongoClient
from twitter import store_tweets
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler
from bson import json_util 
import atexit
import json

# Define our app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# This is our cron job for getting tweets
scheduler = BackgroundScheduler()
scheduler.add_job(func=store_tweets, trigger="interval", minutes=10)
scheduler.start()

# Shutdown cronjob if process is stopped
atexit.register(lambda: scheduler.shutdown(wait=False))

# Connect to our database
client = MongoClient("mongodb+srv://ee461l-blog:trapdungeon@cluster0-1mz2k.mongodb.net/test?retryWrites=true&w=majority")
db = client['tsentimeter']

@app.route("/")
def hello():
    return "Hello World!"

# This end point returns all tweets for a given topic
@app.route("/tweets/topic/<topic>")
def tweets_topic(topic):
    tweets = db.tweets.find({"topic": topic})

    response = app.response_class(
        response=json_util.dumps(tweets[0]),
        status=200
    )

    return response

if __name__ == '__main__':
    app.run(debug=True)
