from bs4 import BeautifulSoup, Comment
from torpy.http.requests import TorRequests
import requests
import re
from urllib.parse import urljoin
from utils import logger
import time

class HtmlFetcher:
    def __init__(self, torpy_manager):
        self.torpy_manager = torpy_manager
    
    @logger
    def create_letter_url(self, letter):

        query = f'https://www.azlyrics.com/{letter}.html'

        return query

    @logger
    def get_artist_urls(self, url, AGENT_LIST):    
        urls = []
        
        response = self.torpy_manager.request_handler(url, AGENT_LIST) 
        print(response.text)

        if self.torpy_manager.check_for_captcha(response):
            time.sleep(5)
            cap_count = 0
            while self.torpy_manager.check_for_captcha(response) or cap_count <= 3:
                print("CAPTCHA detected. Creating a new session.")
                with TorRequests() as tor_requests:
                    with tor_requests.get_session() as sess:
                        self.torpy_manager.rotate_session(sess)
                        response = self.torpy_manager.request_handler(url, AGENT_LIST)
                        cap_count += 1

        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            divs = soup.find_all('div', class_='col-sm-6 text-center artist-col')
            
            for div in divs:
                for a_tag in div.find_all('a'):
                    link = a_tag.get('href')
                    if link:
                        absolute_link = urljoin(url, link)
                        urls.append(absolute_link)
        else:
            print("No Response Found.")
        
        return urls

    @logger
    def get_song_urls(self, url, AGENT_LIST):    
        urls = []
        
        response = self.torpy_manager.request_handler(url, AGENT_LIST)
        print(response.text)

        if self.torpy_manager.check_for_captcha(response):
            cap_count = 0
            while self.torpy_manager.check_for_captcha(response) or cap_count <= 3:
                print("CAPTCHA detected. Creating a new session.")
                with TorRequests() as tor_requests:
                    with tor_requests.get_session() as sess:
                        self.torpy_manager.rotate_session(sess)
                        response = self.torpy_manager.request_handler(url, AGENT_LIST)
                        cap_count += 1

        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            divs = soup.find_all('div', class_='listalbum-item')
            
            for div in divs:
                for a_tag in div.find_all('a'):
                    link = a_tag.get('href')
                    if link:
                        absolute_link = urljoin(url, link)
                        urls.append(absolute_link)
        else:
            print("No Response Found.")
                        
        return urls
    
    @logger
    def get_lyrics_from_url(self, url, AGENT_LIST):
        
        response = self.torpy_manager.request_handler(url, AGENT_LIST) 
        print(response.text)
        
        if self.torpy_manager.check_for_captcha(response):
            cap_count = 0
            while self.torpy_manager.check_for_captcha(response) or cap_count <= 3:
                print("CAPTCHA detected. Creating a new session.")
                with TorRequests() as tor_requests:
                    with tor_requests.get_session() as sess:
                        self.torpy_manager.rotate_session(sess)
                        response = self.torpy_manager.request_handler(url, AGENT_LIST)
                        cap_count += 1

        if response:
        
            soup = BeautifulSoup(response.text, 'html.parser')

            def find_lyrics_div(tag):
                for elem in tag(text=lambda text: isinstance(text, Comment)):    
                    if "Usage of azlyrics.com content by any third-party lyrics provider is prohibited" in elem:
                        return True
                return False

            lyrics_div = soup.find(find_lyrics_div)

            if lyrics_div:

                for elem in lyrics_div(text=lambda text: isinstance(text, Comment)):
                    elem.extract()

                lyrics = '\n'.join(line.strip() for line in lyrics_div.stripped_strings)

                return lyrics

            else:
                return "Lyrics div not found"
            
        else:
            print("No Lyrics Found")
            return None
