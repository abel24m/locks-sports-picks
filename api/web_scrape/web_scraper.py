from datetime import datetime, timedelta
from api.web_scrape.support.save_data import save_mlb_data
import threading

from api.web_scrape.analyst.analyst import Analyst
from api.web_scrape.web_scrapers.covers_scraper import CoversScraper
from support.csv_writer import CSVWriter
from web_scrapers.bovada_scraper import BovadaWebScraper

today_date = datetime.now().strftime("%m-%d-%Y")
yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%m-%d-%Y")

today_file_path = f"./web_scrape/output/bovada_scrape_{today_date}.csv"
# yesterday_file_path = f"/text_files/bovada_scrape_{yesterday_date}.csv"

leagues_to_scrape = ["MLB"]


def initiate_web_scrape():
    bov_scraper = BovadaWebScraper(leagues_to_scrape)
    cover_scraper = CoversScraper(leagues_to_scrape)
    analyst = Analyst()
    bov_scraper.start_scrape()
    cover_scraper.start_scrape()
    analyst.analyze_mlb(cover_scraper.mlb_matches)
    save_mlb_data(cover_scraper.mlb_matches)


# web_scrape()

    # schedule.every().day.at("10:30").do(web_scrape)

if __name__ == "__main__":
    initiate_web_scrape()