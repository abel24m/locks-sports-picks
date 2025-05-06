import json
from datetime import datetime

from api.web_scrape.data.covers_baseball_match_data import CoversBaseballMatchData


def save_mlb_data(matches : [CoversBaseballMatchData]):
    today_date = datetime.now().strftime("%m-%d-%Y")
    filename = f"covers_mlb_data_{today_date}.json"
    file_path = f"./web_scrape/data_storage/{filename}"
    with open(file_path, "a") as file :
        all_games = []
        match : CoversBaseballMatchData
        for match in matches:
            dump = match.get_json_dump()
            all_games.append(dump)
        json.dump(all_games, file, indent=2)

    print("json dumped")
