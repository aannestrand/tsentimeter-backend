# app.py
from flask import Flask
from scripts.twitter import store_tweets
from crontab import CronTab

app = Flask(__name__)

cron = CronTab(user='username')
job = cron.new(command='python example1.py')
job.minute.every(1)
cron.write()

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)