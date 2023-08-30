import pandas as pd
from bs4 import BeautifulSoup, Comment
import re
from utils import logger 

class DataHandler:
    def __init__(self, html_fetcher, torpy_manager):
        self.html_fetcher = html_fetcher 
        self.torpy_manager = torpy_manager  
        self.lyric_df = pd.DataFrame(columns=["artist_url", "song_url", "lyrics", "letter"]) 
    
    @logger
    def store_data(self, artist_url, song_url, clean_lyrics, letter):
        new_row_df = pd.DataFrame([{"artist_url": artist_url,
                                    "song_url": song_url,
                                    "lyrics": clean_lyrics,
                                    "letter": letter}])
        self.lyric_df = pd.concat([self.lyric_df, new_row_df], ignore_index=True)
    
    @logger
    def save_to_csv(self, file_path):
        self.lyric_df.to_csv(file_path, index=False)
        
    '''
    @logger
    def get_lyrics_from_url(self, url, AGENT_LIST):
        response = self.torpy_manager.request_handler(url, AGENT_LIST) 
        
        if response:
            lyrics_div = self.find_lyrics_div(response.text)
            if lyrics_div:
                cleaned_lyrics = self.clean_lyrics(lyrics_div)
                return cleaned_lyrics
            else:
                print("Lyrics Div Not Found")
                return None
        else:
            print("No Lyrics Found")
            return None
    
    def find_lyrics_div(self, tag):
        for elem in tag(text=lambda text: isinstance(text, Comment)):    
            if "Usage of azlyrics.com content by any third-party lyrics provider is prohibited" in elem:
                return True
        return False
    
    '''
    
    @logger
    def clean_lyrics(self, raw_text):

        start_index = raw_text.find("\nSearch")
        if start_index == -1:
            print("Start marker not found")
            return None

        end_index = raw_text.find("\nSubmit Corrections")
        if end_index == -1:
            print("End marker not found")
            return None

        lyrics = raw_text[start_index + len("\nSearch"):end_index].strip()
        
        cleaned_lyrics = re.sub(r'\[.*?(Chorus|Intro|Verse|Bridge|Outro|Hook|Pre-Chorus|Interlude|Refrain).*?\]', '', lyrics, flags=re.IGNORECASE)
        
        lines = cleaned_lyrics.split('\n')[3:]
        cleaned_lyrics = '\n'.join(lines)

        return cleaned_lyrics.strip()
