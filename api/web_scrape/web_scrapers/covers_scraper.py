from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List

from api.web_scrape.data.covers_baseball_match_data import CoversBaseballMatchData
from api.web_scrape.support import globals


class CoversScraper:

    covers_today_date = datetime.now().strftime("%Y-%m-%d")

    urls = {
        "NBA" : f"https://www.covers.com/sports/nba/matchups?selectedDate={covers_today_date}",
        "NCAAB" : f"https://www.covers.com/sports/ncaab/matchups?selectedDate={covers_today_date}",
        "MLB" : f"https://www.covers.com/sports/mlb/matchups?selectedDate={covers_today_date}"
    }

    mlb_matches : [CoversBaseballMatchData]


    def __init__(self, leagues: List[str]):
        self.leagues = leagues
        self.driver = webdriver.Chrome()
        self.mlb_matches = []

    def start_scrape(self):
        for league in self.leagues:
            match league:
                case("MLB"):
                    try:
                        self._scrape_mlb()
                    except TimeoutException:
                        print (f"Bovada MLB url took too much time to load!")

    def _scrape_all_games(self, league : str):
        match_href = []
        # Scrape all the match hrefs from the matches page
        try:
            self.driver.get(self.urls.get(league))
            WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pregamebox")))
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a.matchup-btn-link")
            for elem in elements:
                ref = elem.get_attribute("href")
                match_href.append(ref)
        except TimeoutException:
            print("Loading Matches Page took too long")
        return match_href

    def _scrape_mlb(self):
        all_game_href = self._scrape_all_games("MLB")
        # Iterate through every match href. Each href is a match page
        for game in all_game_href:
            try:
                self.driver.get(game)
                WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'away']")))
            except TimeoutException:
                print(f"{game} could not be scraped")
                continue

            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            match = CoversBaseballMatchData()

            # scrape time
            time = soup.find("span", {"class": "matchup-time"}).text.split()
            match.match_time = time[0]

            # Scrape Names of Teams and Short Names for future ref
            match.away_team= soup.find("span", {"data-team": "away", "class": "display-name"}).text
            match.home_team = soup.find("span", {"data-team": "home", "class": "display-name"}).text
            match.away_team_short = soup.find("span", {"data-team": "away", "class": "short-name"}).text
            match.home_team_short = soup.find("span", {"data-team": "home", "class": "short-name"}).text

            # Scrape Head-to-Head data
            head_to_head_elem = soup.find("section", {"class": "both-team-section"})
            self._scrape_mlb_hth(head_to_head_elem, match)

            # Scrape past games data from both teams.
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'away']")))
            self.driver.find_element(By.CSS_SELECTOR, "button[data-team = 'away']").send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "section[class = 'away-team-section']")))
            away_team_section = soup.find("section", {"class": "away-team-section"})

            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'home']")))
            self.driver.find_element(By.CSS_SELECTOR, "button[data-team = 'home']").send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "section[class = 'home-team-section']")))
            home_team_section = soup.find("section", {"class": "home-team-section"})
            self._scrape_mlb_teams_lt(away_team_section, home_team_section, match)

            #Scrape Pitcher Data
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-controls = 'away-team-last-5'][role = 'tab']")))
            self.driver.find_element(By.CSS_SELECTOR, "a[aria-controls = 'away-team-last-5'][role = 'tab']").send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[role = 'tabpanel'][id = 'away-team-last-5']")))
            away_pitcher_section = soup.find("div", {"role": "tabpanel", "id": "away-team-last-5"})

            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-controls = 'home-team-last-5'][role = 'tab']")))
            self.driver.find_element(By.CSS_SELECTOR, "a[aria-controls = 'home-team-last-5'][role = 'tab']").send_keys(
                Keys.ENTER)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div[role = 'tabpanel'][id = 'home-team-last-5']")))
            home_pitcher_section = soup.find("div", {"role": "tabpanel", "id": "home-team-last-5"})

            self._scrape_pitcher(away_pitcher_section, match, "away")
            self._scrape_pitcher(home_pitcher_section, match, "home")

            #Scrape Hitting and Pitching Averages
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-controls = 'hitting'][role = 'tab']")))
            self.driver.find_element(By.CSS_SELECTOR, "a[aria-controls = 'hitting'][role = 'tab']").send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[role = 'tabpanel'][id = 'hitting']")))
            self.driver.find_element(By.CSS_SELECTOR, "button[data-toggle = 'dropdown'][id = 'props-event-btn']").send_keys(Keys.ENTER)
            drop_down_list = self.driver.find_element(By.CSS_SELECTOR, "ul[class = 'dropdown-menu'][id = 'stats-analysis-split']")
            drop_down_items = drop_down_list.find_elements(By.CSS_SELECTOR, "li[class = 'split-type']")
            #Index 3 should be "last 10" option.
            drop_down_items[3].click()
            WebDriverWait(self.driver, 10).until(EC.staleness_of(self.driver.find_element(By.CSS_SELECTOR, "div[role = 'tabpanel'][id = 'hitting']")))
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role = 'tabpanel'][id = 'hitting']")))
            new_soup = BeautifulSoup(self.driver.page_source, "html.parser")
            hitting_table_elem = new_soup.find("div", {"class" : "tab-pane", "id" : "hitting"})
            self._scrape_hitting(hitting_table_elem, match)

            #Scrape Bullpen Data
            bullpen_elem = new_soup.find("div", {"id" : "bullpen"})
            self._scrape_bullpen(bullpen_elem, match)

            self.mlb_matches.append(match)


    @staticmethod
    def _scrape_bullpen_table(bullpen_table : BeautifulSoup):
        rows = bullpen_table.find_all("tr")
        # get data from last row
        num_rows = len(rows)
        data = rows[num_rows-1].find_all("td")
        bullpen_era = data[10].text
        bullpen_whip = data[11].text
        result = {
            globals.BULLPEN_ERA : bullpen_era,
            globals.BULLPEN_WHIP : bullpen_whip
        }
        return result

    def _scrape_bullpen(self, bullpen_elem : BeautifulSoup, match : CoversBaseballMatchData):
        bullpen_tables = bullpen_elem.find_all("table", {"class" : "bullpen-table"})
        away_bullpen_table = bullpen_tables[0]
        home_bullpen_table = bullpen_tables[1]
        away_bullpen_data = self._scrape_bullpen_table(away_bullpen_table)
        home_bullpen_data = self._scrape_bullpen_table(home_bullpen_table)
        match.set_bullpen_data(home_bullpen_data,away_bullpen_data)


    def _scrape_hitting(self, hitting_elem : BeautifulSoup, match : CoversBaseballMatchData):
        table_body = hitting_elem.find("tbody")
        table_rows  = table_body.find_all("tr")
        away_team_row = table_rows[0]
        home_team_row = table_rows[1]
        away_hitting_dict = self._scrape_hitting_row(away_team_row)
        home_hitting_dict = self._scrape_hitting_row(home_team_row)
        sleep(10)
        match.set_hitting_data(home_hitting_dict, away_hitting_dict)
        # Away team is row one and Home team is row two

    @staticmethod
    def _scrape_hitting_row(row : BeautifulSoup):
        stats = row.find_all("td")
        runs_avg = stats[1].text
        bat_avg = stats[2].text
        hits_avg = stats[3].text
        hr_avg = stats[4].text
        bb_avg = stats[5].text
        result = {
            globals.HITTING_RUNS_AVG : runs_avg,
            globals.HITTING_HITS_AVG : hits_avg,
            globals.HITTING_HR_AVG : hr_avg,
            globals.HITTING_BATTING_AVG : bat_avg,
            globals.HITTING_BB_AVG : bb_avg
        }
        return result





    @staticmethod
    def _scrape_mlb_hth(hth_elem: BeautifulSoup, match: CoversBaseballMatchData):
        betting_record_elem = hth_elem.find_all("div", {"class" : "record-value"})
        win_loss_record = betting_record_elem[0].text
        over_under_record = betting_record_elem[1].text.strip()
        hth = {
            globals.HTH_WIN_LOSS: win_loss_record,
            globals.HTH_OVER_UNDER : over_under_record
        }
        match.set_hth_data(hth)

    @staticmethod
    def _scrape_mlb_teams_lt(away_team_lt_elem : BeautifulSoup, home_team_lt_elem: BeautifulSoup, match : CoversBaseballMatchData):
        away_betting_record_elem = away_team_lt_elem.find_all("div", {"class": "record-value"})
        home_betting_record_elem = home_team_lt_elem.find_all("div", {"class": "record-value"})
        away_win_loss_record = away_betting_record_elem[0].text
        away_over_under_record = away_betting_record_elem[1].text.strip()
        home_win_loss_record = home_betting_record_elem[0].text
        home_over_under_record = home_betting_record_elem[1].text.strip()
        team_records = {
            "home" : {
                globals.TEAM_WIN_LOSS: home_win_loss_record,
                globals.TEAM_OVER_UNDER: home_over_under_record
            },
            "away" : {
                globals.TEAM_WIN_LOSS: away_win_loss_record,
                globals.TEAM_OVER_UNDER: away_over_under_record
            }
        }
        match.set_team_betting_records(team_records)

    @staticmethod
    def _scrape_pitcher(pitcher_section : BeautifulSoup, match : CoversBaseballMatchData, match_side: str):
        #Scrape Betting Records that are above the table of last 5 games
        betting_records = pitcher_section.find_all("div", {"class": "record-value"})
        pitcher_win_loss = betting_records[0].text
        pitcher_era = betting_records[1].text
        pitcher_ip = betting_records[2].text

        #Scrape the averages of the last 5
        last_five_avg_table = pitcher_section.find("table", {"class" : "starter-table"})
        table_rows = last_five_avg_table.find_all("tr")
        if len(table_rows) <= 2:
            return
        last_row = table_rows[len(table_rows)-1]
        fields_in_row = last_row.find_all("td")
        pitcher_hits = fields_in_row[4].text
        pitcher_runs = fields_in_row[5].text
        pitcher_er = fields_in_row[6].text
        pitcher_so = fields_in_row[7].text
        pitcher_bb = fields_in_row[8].text
        pitcher_hr = fields_in_row[9].text
        pitcher_pit = fields_in_row[10].text
        pitcher_pip = fields_in_row[11].text
        result = {
            globals.PITCHER_WIN_LOSS : pitcher_win_loss,
            globals.PITCHER_ERA : pitcher_era,
            globals.PITCHER_IP : pitcher_ip,
            globals.PITCHER_HITS : pitcher_hits,
            globals.PITCHER_RUNS : pitcher_runs,
            globals.PITCHER_ER : pitcher_er,
            globals.PITCHER_SO : pitcher_so,
            globals.PITCHER_BB : pitcher_bb,
            globals.PITCHER_HR : pitcher_hr,
            globals.PITCHER_PIT : pitcher_pit,
            globals.PITCHER_PIP : pitcher_pip
        }
        match match_side:
            case "away":
                match.set_away_pitcher_data(result)
            case "home":
                match.set_home_pitcher_data(result)









if __name__ == "__main__":
    lol = ["MLB"]
    obj = CoversScraper(lol)
    obj.start_scrape()





