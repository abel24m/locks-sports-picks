from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List

from api.web_scrape.data.bovada_data import BovadaData


class BovadaWebScraper:

    __urls = {
        "NCAAB": {
            "https://www.bovada.lv/sports/basketball/college-basketball",
            "https://www.bovada.lv/sports/basketball/ncaa-nit"
        },
        "NBA": {
            "https://www.bovada.lv/sports/basketball/nba"
        },
        "MLB": {
            "https://www.bovada.lv/sports/baseball/mlb"
        }
    }

    __leagues_to_write = {
        "NCAAB" : False,
        "NBA" : False,
        "MLB" : False
    }


    today_date = datetime.now().strftime("%m-%d-%Y")
    delay = 10
    ncaab_matches = []
    mlb_games = []
    nba_games = []


    def __init__(self, list_of_leagues: List[str]):
        self.driver = webdriver.Chrome()
        self.leagues = list_of_leagues


    def start_scrape(self):
        for league in self.leagues:
            match league:
                # case("NCAAB"):
                #     try:
                #         self.scrape_ncaab()
                #     except TimeoutException:
                #         print (f"Bovada NCAAB url took too much time to load!")
                # case("NBA"):
                #     try:
                #         delay = 15
                #         for url in self.__urls.get("NBA"):
                #             self.driver.get(url)
                #             WebDriverWait(BovadaWebScraper.driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "sp-next-events[waiting-for-files-to-load = 'success!']")))
                #             self.scrape_nba()
                #     except TimeoutException:
                #         print (f"Bovada NBA url took too much time to load!")
                case("MLB"):
                    try:
                        self.scrape_mlb()
                    except TimeoutException:
                        print (f"Bovada MLB url took too much time to load!")

    @staticmethod
    def make_team_string(words):
        team = ""
        for word in words:
            team += word + " "
        return team.strip()

    def get_leagues_to_write(self):
        return self.__leagues_to_write

    def get_league_data(self, league: str):
        match league :
            case("MLB"):
                return self.mlb_games
            case("NBA"):
                return self.nba_games
            case _:
                return

    def scrape_mlb(self):
        url_set = self.__urls.get("MLB")
        for url in url_set:
            self.driver.get(url)
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "sp-next-events[waiting-for-files-to-load = 'success!']")))
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            game_elements = soup.select('section.coupon-content')
            current_date = datetime.now().strftime("%-m/%d/%y").strip()
            for game in game_elements:
                date = game.find("span", {"class" : "period hidden-xs"}).text.strip()
                date_elements = date.split()
                if date_elements[0] != current_date:
                    # if the game is not today then skip to the next game.
                    continue
                teams = game.find_all("span", {"class": "name"})
                home_team_words = teams[1].text.split()
                away_team_words = teams[0].text.split()
                away_team_words_cleaned = [y for y in away_team_words if "#" not in y]
                home_team_words_cleaned = [y for y in home_team_words if "#" not in y]
                home_team = self.make_team_string(home_team_words_cleaned)
                away_team = self.make_team_string(away_team_words_cleaned)
                spreads = game.find_all("span", {"class" : "market-line bet-handicap"})
                allOdds = game.find_all("span", {"class" : "bet-price"})
                moneylineOdds = [odd for odd in allOdds if "(" not in odd.get_text()]
                total_elem =  game.find("span", {"class" : "market-line bet-handicap both-handicaps"})
                home_spread = spreads[1].text
                away_spread = spreads[0].text
                home_ml_odds = moneylineOdds[1].text
                away_ml_odds = moneylineOdds[0].text
                total = total_elem.text
                bov_mlb_game = BovadaData(date, home_team, away_team, home_spread, away_spread, home_ml_odds, away_ml_odds, total)
                self.mlb_games.append(bov_mlb_game)
        self.__leagues_to_write["MLB"] = True


    def scrape_nba(self):
        # # check if file for today already exists
        today_date = datetime.now().strftime("%m-%d-%Y")
        # today_file = Path(bov_file"./output_files/bovadaScrape-NBA-{today_date}.csv")
        # if file exist then return
        # if today_file.is_file():
        #     print("Bovada already scraped for today")
        #     return
        #if not then scrape bovada
        html = self.driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        game_elements = soup.select('sp-coupon')
        bov_file = open(f"./text_files/bovada_scrape_{today_date}.csv", "a")

        #iterate through every row that contains a matchup
        for game in game_elements:
            date = game.find("span", {"class" : "period hidden-xs"}).text
            teams = game.findAll("span", {"class": "name"})
            home_team_words = teams[1].text.split()
            away_team_words = teams[0].text.split()
            away_team_words_cleaned = [y for y in away_team_words if "#" not in y]
            home_team_words_cleaned = [y for y in home_team_words if "#" not in y]
            home_team = self.make_team_string(home_team_words_cleaned)
            away_team = self.make_team_string(away_team_words_cleaned)
            spreads = game.findAll("span", {"class" : "market-line bet-handicap"})
            total_elem =  game.find("span", {"class" : "market-line bet-handicap both-handicaps"})
            home_spread = spreads[1].text
            away_spread = spreads[0].text
            total = total_elem.text
            bov_ncaab_game = BovadaData(date, home_team, away_team, home_spread, away_spread, "", "", total)
            self.ncaab_matches.append(bov_ncaab_game)

            bov_file.write((home_team + ", " + home_spread +", ").replace(chr(0xA0), ' '))
            bov_file.write((away_team + ", " + away_spread +", ").replace(chr(0xA0), ' '))
            bov_file.write((total + ", "))
            bov_file.write(date.strip()+"\n")
        bov_file.close()


    # def scrape_ncaab(self):
    #     delay = 15
    #     # check if file for today already exists
    #     today_date = datetime.now().strftime("%m-%d-%Y")
    #     today_file = Path(f"./output_files/bovadaScrape-NCAAB-{today_date}.csv")
    #     # if file exist then return
    #     if today_file.is_file():
    #         print("Bovada already scraped for today")
    #         return
    #     f = open(f"./output_files/bovadaScrape-NCAAB-{today_date}.csv", "w")
    #     for url in self.ncaab_urls:
    #         self.driver.get(url)
    #         WebDriverWait(BovadaWebScraper.driver, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "sp-next-events[waiting-for-files-to-load = 'success!']")))
    #         html = self.driver.page_source
    #         soup = BeautifulSoup(html,"html.parser")
    #         game_elements = soup.select('sp-coupon')
    #         current_date = datetime.now().strftime("%-m/%d/%y").strip()
    #         #iterate through every row that contains a matchup
    #         for game in game_elements:
    #             date = game.find("span", {"class" : "period hidden-xs"}).text.strip()
    #             date_elements = date.split()
    #             if date_elements[0] != current_date:
    #                 continue
    #             teams = game.findAll("span", {"class": "name"})
    #             home_team_words = teams[1].text.split()
    #             away_team_words = teams[0].text.split()
    #             away_team_words_cleaned = [y for y in away_team_words if "#" not in y]
    #             home_team_words_cleaned = [y for y in home_team_words if "#" not in y]
    #             home_team = self.make_team_string(home_team_words_cleaned)
    #             away_team = self.make_team_string(away_team_words_cleaned)
    #             spreads = game.findAll("span", {"class" : "market-line bet-handicap"})
    #             total_elem =  game.find("span", {"class" : "market-line bet-handicap both-handicaps"})
    #             home_spread = spreads[1].text
    #             away_spread = spreads[0].text
    #             total = total_elem.text
    #             bov_ncaab_game = BovadaData(date, home_team, away_team, home_spread, away_spread, "", "", total)
    #             self.ncaab_matches.append(bov_ncaab_game)
    #
    #             f.write((home_team + ", " + home_spread +", ").replace(chr(0xA0), ' '))
    #             f.write((away_team + ", " + away_spread +", ").replace(chr(0xA0), ' '))
    #             f.write((total + ", "))
    #             f.write(date.strip()+"\n")
    #     f.close()

# if __name__ == "__main__" :
#     lol = ["MLB"]
#     bov_scraper = BovadaWebScraper(lol)
#     bov_scraper.start_scrape()
