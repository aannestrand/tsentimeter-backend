# app.py
from flask import Flask
from crontab import CronTab

cron.write()
app = Flask(__name__)

cron = CronTab(user='tweeter')
job = cron.new(command='python /scripts/twitter.py')
job.minute.every(1)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)