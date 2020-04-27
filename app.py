# app.py
from flask import Flask
from scripts.twitter import store_tweets
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(func=store_tweets, trigger="interval", minutes=10)
scheduler.start()

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
