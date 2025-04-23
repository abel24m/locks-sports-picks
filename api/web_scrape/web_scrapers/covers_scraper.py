from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List


class CoversScraper:

    covers_today_date = datetime.now().strftime("%Y-%m-%d")

    urls = {
        "NBA" : f"https://www.covers.com/sports/nba/matchups?selectedDate={covers_today_date}",
        "NCAAB" : f"https://www.covers.com/sports/ncaab/matchups?selectedDate={covers_today_date}",
        "MLB" : f"https://www.covers.com/sports/mlb/matchups?selectedDate={covers_today_date}"
    }


    def __init__(self, leagues: List[str]):
        self.leagues = leagues
        self.driver = webdriver.Chrome()

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
            match = CoversBasketballMatchData()

            # scrape time
            time = soup.find("span", {"class": "matchup-time"}).text.split()
            match.time = time[0]

            # Scrape Names of Teams and Short Names for future ref
            away_team_name = soup.find("span", {"data-team": "away", "class": "display-name"}).text
            home_team_name = soup.find("span", {"data-team": "home", "class": "display-name"}).text
            away_team_name_short = soup.find("span", {"data-team": "away", "class": "short-name"}).text
            home_team_name_short = soup.find("span", {"data-team": "home", "class": "short-name"}).text

            # Scrape Head to Head data
            head_to_head_elem = soup.find("section", {"class": "both-team-section"})
            hth_stats = PastGames()
            CoversWebScraper.scrape_head_to_head(head_to_head_elem, hth_stats, home_team_name_short,
                                                 away_team_name_short)
            match.hth_history = hth_stats

            # Scrape past games data from both teams.
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'away']")))
            self.driver.find_element(By.CSS_SELECTOR, "button[data-team = 'away']").send_keys(Keys.ENTER)
            away_team_section = soup.find("section", {"class": "away-team-section"})
            away_past_games = PastGames()
            CoversWebScraper.scrape_past_games(away_team_section, away_past_games, away_team_name_short)
            match.away_team_past = away_past_games

            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-team = 'home']")))
            self.driver.find_element(By.CSS_SELECTOR, "button[data-team = 'home']").send_keys(Keys.ENTER)
            home_team_section = soup.find("section", {"class": "home-team-section"})
            home_past_games = PastGames()
            CoversWebScraper.scrape_past_games(home_team_section, home_past_games, home_team_name_short)
            match.home_team_past = home_past_games

            # Create Home and Away Teams assign name and short names
            away_team = CoversBasketballTeamData()
            away_team.team = away_team_name
            away_team.team_short = away_team_name_short
            home_team = CoversBasketballTeamData()
            home_team.team = home_team_name
            home_team.team_short = home_team_name_short

            away_key_stats = soup.find("section", {"aria-labelledby": "key-stats"})
            CoversWebScraper.scrape_key_stats(away_key_stats, away_team, home_team)
            away_more_stats = soup.find("section", {"aria-labelledby": "more-stats"})
            CoversWebScraper.scrape_more_stats(away_more_stats, away_team, home_team)
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href = '#home-team-offense']")))
            self.driver.find_element(By.CSS_SELECTOR, "a[href = '#home-team-offense']").send_keys(Keys.ENTER)
            attempts = 0
            while attempts < 6:
                try:
                    WebDriverWait(self.driver, 15).until(EC.visibility_of_all_elements_located(
                        (By.CSS_SELECTOR, "div[id = 'home-team-offense'][class = 'tab-pane fade in active']")))
                    break
                except TimeoutException:
                    print(f"home team stats never loaded for {href}")
                    attempts += 1
            if attempts == 6:
                continue
            new_soup = BeautifulSoup(self.driver.page_source, "html.parser")
            home_key_stats = new_soup.findAll("section", {"aria-labelledby": "key-stats"})
            CoversWebScraper.scrape_key_stats(home_key_stats[1], home_team, away_team)
            home_more_stats = new_soup.findAll("section", {"aria-labelledby": "more-stats"})
            CoversWebScraper.scrape_more_stats(home_more_stats[1], home_team, away_team)
            match.home_stats = home_team
            match.away_stats = away_team
            match.analyze_key_stats()
            match.analyze_more_stats()
            match.analyze_past_games()
            all_games.append(match)
        return all_games







if __name__ == "__main__":
    lol = ["MLB"]
    obj = CoversScraper(lol)
    obj.start_scrape()





