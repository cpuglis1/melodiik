from scrape_az import ScrapeAZ
from html_fetcher import HtmlFetcher
from torpy_manager import TorpyManager
from data_handler import DataHandler
from config import alphabet, AGENT_LIST 
from utils import timer_decorator  

@timer_decorator  
def main():
    torpy_manager = TorpyManager()
    html_fetcher = HtmlFetcher(torpy_manager)
    data_handler = DataHandler(html_fetcher, torpy_manager)
    
    scraper = ScrapeAZ(html_fetcher, torpy_manager, data_handler)
    
    result_df = scraper.scrape_az_lyrics(alphabet, AGENT_LIST)
    
    result_df.to_csv("lyrics_data_test3.csv")

if __name__ == "__main__":
    main()
