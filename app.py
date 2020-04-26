from flask import Flask
app = Flask(__name__)


# This is our main route
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()