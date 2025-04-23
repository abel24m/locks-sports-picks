import time

import schedule
from flask import Flask

app = Flask(__name__)

# schedule.every().day.at("10:30").do(web_scrape)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/nba')
def get_nba_games():
    with open("test.txt", "r") as f:
        content = f.readline()
    return {'data': content}