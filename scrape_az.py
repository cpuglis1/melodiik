import pandas as pd
from utils import logger
from torpy.http.requests import TorRequests

class ScrapeAZ:
    def __init__(self, html_fetcher, torpy_manager, data_handler):
        self.html_fetcher = html_fetcher
        self.torpy_manager = torpy_manager
        self.data_handler = data_handler

    @logger
    def scrape_az_lyrics(self, alphabet, AGENT_LIST):
        counter = 0
        

        with TorRequests() as tor_requests:
            with tor_requests.get_session() as sess:
                self.torpy_manager.create_session(sess)

                for letter in alphabet:
                    letter_url = self.html_fetcher.create_letter_url(letter)
                    artist_urls = self.html_fetcher.get_artist_urls(letter_url, AGENT_LIST)

                    self.torpy_manager.check_and_rotate_session(sess)
                    
                    for artist_url in artist_urls:
                        song_urls = self.html_fetcher.get_song_urls(artist_url, AGENT_LIST)
                        
                        self.torpy_manager.check_and_rotate_session(sess)
                        
                        for song_url in song_urls:
                            raw_html = self.html_fetcher.get_lyrics_from_url(song_url, AGENT_LIST)
                            clean_html = self.data_handler.clean_lyrics(raw_html)

                            self.data_handler.store_data(artist_url, song_url, clean_html, letter)
                            
                            self.torpy_manager.check_and_rotate_session(sess)

                            counter += 1
                            if counter >= 3:
                                self.torpy_manager.close_session()
                                return self.data_handler.lyric_df

                self.torpy_manager.close_session()
                return self.data_handler.lyric_df
