from api.web_scrape.data.bovada_data import BovadaData
from api.web_scrape.web_scrapers.bovada_scraper import BovadaWebScraper


class CSVWriter:



    def __init__(self, file_path: str):
        self.file = open(file_path, "w")


    def write_bovada_data(self, bovada_data : BovadaWebScraper):
        leagues_to_write = bovada_data.get_leagues_to_write()
        for league, writing in leagues_to_write.items():
            if writing:
                self.file.write(league + "\n")
                games = bovada_data.get_league_data(league)
                game : BovadaData
                for game in games:
                    self.file.write(game.write_csv())
