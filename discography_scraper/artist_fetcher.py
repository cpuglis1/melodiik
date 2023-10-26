import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.parse

class ArtistFetcher:
    def __init__(self, base_link: str, number_of_pages: int, genre: str):
        self.base_link = base_link
        self.number_of_pages = number_of_pages
        self.genre = genre

    def get_artist_names(self, url: str) -> list:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        artist_names = []
        
        for a in soup.find_all('a', href=True):
            if a['href'].startswith('/music/'):
                url_name = a['href'].replace('/music/', '')
                cleaned_name = urllib.parse.unquote(url_name).replace('+', ' ') 
                artist_names.append((cleaned_name, url_name))
        
        return artist_names

    def clean_name(self, artist_names: list) -> list:
        cleaned_names = [urllib.parse.unquote(name).replace('+', ' ') for name in artist_names if name != '+free-music-downloads']
        unique_names = list(dict.fromkeys(cleaned_names))
        return unique_names

    def fetch_artists(self) -> set:
        all_artists = []
        
        for i in range(self.number_of_pages):
            url = self.base_link + str(i+1)
            all_artists.extend(self.get_artist_names(url))

        url_artist_list = set(all_artists)
        url_artist_list = {tup for tup in url_artist_list if tup[1] != '+free-music-downloads'}
        
        return url_artist_list

    def convert_to_dataframe(self, url_artist_list):
        data = [
            (*artist_info, self.genre) for artist_info in url_artist_list
        ]
        
        df = pd.DataFrame(data, columns=['artist name', 'url artist name', 'genre'])
        df = df.groupby(['artist name', 'url artist name'])['genre'].apply(', '.join).reset_index()
        df = df[~df['artist name'].str.contains("free-music-downloads")]
        df['genre'] = df['genre'].str.split(', ').apply(set).str.join(', ')
        
        return df

base_link = 'https://www.last.fm/tag/bedroom+pop/artists?page='
number_of_pages = 3
fetcher = ArtistFetcher(base_link, number_of_pages, 'dream pop')
artists = fetcher.fetch_artists()
df = fetcher.convert_to_dataframe(artists)
print(df.head())