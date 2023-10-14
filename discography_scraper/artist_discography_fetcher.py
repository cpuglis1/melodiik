import requests
import pandas as pd
from bs4 import BeautifulSoup

class ArtistDetailFetcher:
    def __init__(self, base_artist_url, album_url_addition, df):
        self.base_artist_url = base_artist_url
        self.album_url_addition = album_url_addition
        self.df = df

    def get_artist_stats(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        listeners_tag = soup.find('h4', string='Listeners')
        listeners = listeners_tag.find_next('abbr', class_='intabbr')['title'] if listeners_tag else "N/A"
        
        scrobbles_tag = soup.find('h4', string='Scrobbles')
        scrobbles = scrobbles_tag.find_next('abbr', class_='intabbr')['title'] if scrobbles_tag else "N/A"

        return listeners, scrobbles

    def get_artist_albums(self, url):
        page_number = 1
        all_album_names = []
        
        while True:
            page_url = f"{url}&page={page_number}"
            response = requests.get(page_url)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            artist_name = url.rstrip('/').split('/')[-2]
            albums_section = soup.find('section', id="artist-albums-section")

            if not albums_section:
                break

            album_links = albums_section.find_all('a', href=lambda x: x and x.startswith(f"/music/{artist_name}/"))
            for link in album_links:
                cleaned_name = link.get_text()
                if cleaned_name not in ["", "Most popular", "By release date"]:
                    url_name = link['href'].split('/')[-1]
                    all_album_names.append((cleaned_name, url_name))

            page_number += 1

        return all_album_names

    def fetch_details(self):
        artist_stats = []
        discography = []

        for artist_url_addition in list(self.df['url artist name']):
            artist_url = self.base_artist_url + artist_url_addition
            artist_listeners, artist_scrobbles = self.get_artist_stats(artist_url)
            artist_tup = (artist_url, artist_listeners, artist_scrobbles)
            artist_stats.append(artist_tup)

            albums_url = artist_url + self.album_url_addition
            album_names = self.get_artist_albums(albums_url)
            albums_tup = (artist_url, album_names)
            discography.append(albums_tup)

        return artist_stats, discography

'''
# Example usage:
base_artist_url = 'https://www.last.fm/music/'
album_url_addition = '/+albums?order=most_popular'

data = {
    'artist name': ['Addison Grace', 'Another Michael', 'Anthony Amorim', 'Black Pool', 'Blue Foster'],
    'url artist name': ['Addison+Grace', 'Another+Michael', 'Anthony+Amorim', 'Black+Pool', 'Blue+Foster'],
    'genre': ['dream pop', 'dream pop', 'dream pop', 'dream pop', 'dream pop']
}

df_p2 = pd.DataFrame(data)

fetcher = ArtistDetailFetcher(base_artist_url, album_url_addition, df_p2)
artist_stats_result, discography_result = fetcher.fetch_details()

print(artist_stats_result)
print()
print(discography_result)
'''