import json

from flask import Flask

app = Flask(__name__)

# schedule.every().day.at("10:30").do(web_scrape)

import os

@app.route('/mlb_data')
def get_current_time():
    with open ("web_scrape/data_storage/covers_mlb_data_05-05-2025.json") as file:
        data = json.load(file)
    return data

@app.route('/nba')
def get_nba_games():
    with open("test.txt", "r") as f:
        content = f.readline()
    return {'data': content}