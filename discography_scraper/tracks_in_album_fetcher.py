# Assuming database_handler.py contains the DatabaseHandler class
from database_handler import DatabaseHandler
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import psycopg2
from tqdm import tqdm
import time

class AlbumProcessor:
    
    def __init__(self, dbname='artist_stats_db', host='localhost', port='5432', start=0, end=10):
        self.db_handler = DatabaseHandler(dbname, host, port) 
        self.dbname = dbname
        self.host = host
        self.port = port
        self.start = start
        self.end = end

    @staticmethod
    def retrieve_tracks_from_album(url):
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        section = soup.find('section', id='tracklist', class_='section-with-separator')
        if not section:
            return []

        base_url_parts = url.split('/')
        if len(base_url_parts) < 5:
            return []
        pattern = "/music/" + base_url_parts[-2] + "/" + base_url_parts[-1]
        track_elements = section.find_all('td', class_='chartlist-name')
        tracks = []

        for track_element in track_elements:
            a_tag = track_element.find('a', href=lambda x: x and x.startswith(pattern))
            if a_tag:
                track_name = a_tag['href'].split('/')[-1]
                chartlist_bar_td = track_element.find_next('td', class_='chartlist-bar')
                if chartlist_bar_td:
                    listeners_span = chartlist_bar_td.find('span', class_='chartlist-count-bar-value')
                    try:
                        if listeners_span:
                            listeners_text = listeners_span.get_text(strip=True)
                            listeners = int(listeners_text.replace('listeners', '').replace('listener', '').replace(',', ''))
                    except ValueError:
                        listeners = 0
                    else:
                        listeners = None
                else:
                    listeners = None

                track_data = {
                    "name": track_name,
                    "listeners": listeners
                }
                tracks.append(track_data)

        metadata_section = soup.find('dl', class_='catalogue-metadata')
        metadata = {}
        if metadata_section:
            headings = metadata_section.find_all('dt', class_='catalogue-metadata-heading')
            descriptions = metadata_section.find_all('dd', class_='catalogue-metadata-description')
            for heading, description in zip(headings, descriptions):
                metadata_key = heading.get_text(strip=True)
                metadata_value = description.get_text(strip=True)
                metadata[metadata_key] = metadata_value

        length = metadata.get('Length')
        release_date = metadata.get('Release Date')
        listeners_tag = soup.find('h4', string='Listeners')
        listeners = listeners_tag.find_next('abbr', class_='intabbr')['title'] if listeners_tag else "N/A"
        scrobbles_tag = soup.find('h4', string='Scrobbles')
        scrobbles = scrobbles_tag.find_next('abbr', class_='intabbr')['title'] if scrobbles_tag else "N/A"
        metadata['Listeners'] = listeners
        metadata['Plays'] = scrobbles
        metadata['AlbumName'] = base_url_parts[-1]
        metadata['Artist'] = base_url_parts[-2]
        return (tracks, metadata)

    @staticmethod
    def process_album(link):
        tracks_and_meta = AlbumProcessor.retrieve_tracks_from_album(link)
        if tracks_and_meta:
            return tracks_and_meta
        return None

    def process(self, max_threads=8):
        start_time = time.time()

        try:
            self.db_handler.connect()
            rows = self.db_handler.select_data("artist_disc") # Use the select_data method
            album_links = [row[-1] for row in rows]
            album_tracks = []

            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                results = list(tqdm(executor.map(self.process_album, album_links[self.start :self.end]), total=len(album_links[self.start:self.end]), desc="Processing albums", unit="album"))
            album_tracks = [result for result in results if result]

            print(album_tracks)

        except Exception as error:
            print(f"Error: {error}")
        
        finally:
            self.db_handler.close() 

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    processor = AlbumProcessor(dbname='artist_stats_db', host='localhost', port='5432', start=5, end=500)

    processor.process()

    

