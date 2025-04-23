from datetime import datetime, timedelta

from support.csv_writer import CSVWriter
from web_scrapers.bovada_scraper import BovadaWebScraper

today_date = datetime.now().strftime("%m-%d-%Y")
yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%m-%d-%Y")

today_file_path = f"./web_scrape/output/bovada_scrape_{today_date}.csv"
# yesterday_file_path = f"/text_files/bovada_scrape_{yesterday_date}.csv"

leagues_to_scrape = ["MLB"]


def initiate_web_scrape():
    bov_scraper = BovadaWebScraper(leagues_to_scrape)
    bov_scraper.start_scrape()
    csv_writer = CSVWriter(today_file_path)
    csv_writer.write_bovada_data(bov_scraper)


# web_scrape()

    # schedule.every().day.at("10:30").do(web_scrape)

if __name__ == "__main__":
    initiate_web_scrape()