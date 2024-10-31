# scripts/scrape_discography.py

import requests
from requests import Response
from bs4 import BeautifulSoup
import logging
import os
import re
import json

class AZArtists:

    def __init__(self, artist: str):
        self.artist = artist
        self.logger = logging.getLogger(__name__)
    
    # Artist formatting
    def _parse_artist(self) -> str: # _ denotes for coder to treat as private method. -> str, annotates return as a string
        self.logger.info(f'Parsing artist {self.artist}')
        return re.sub(r'[^a-z0-9\s]', '', self.artist.lower().replace(' ', ''))
    
    # Dynamic URL method for artist discographies
    def url(self) -> str:
        artist = self._parse_artist().replace('the','')
        url = 'https://www.azlyrics.com/{}/{}.html'\
                .format(artist[0], artist) # \ used to allow newline usage for readability
        self.logger.info(f'Generated URL: {url}')
        return url
    
    # Method to make HTTP request to AZLyrics and return discography
    def open_url(self):
        url = self.url()
        try:
            response = requests.get(url)
            response.raise_for_status() # Raises error for bad responses
            self.logger.info(f'Successfully opened URL: {url}')
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f'HTTP error occurred: {http_err}')
            return None
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f'Connection error occurred: {conn_err}')
            return None
        except requests.exceptions.Timeout as timeout_err:
            self.logger.error(f'Timeout error occurred: {timeout_err}')
            return None
        except requests.exceptions.RequestException as req_err:
            self.logger.error(f'Error occurred during the request: {req_err}')
            return None
    
        if response.ok:
            self._parse_albums(response)
            self.logger.info(f'Successfully saved discography for {self.artist}')
            print(f'Successfully saved discography for {self.artist}')
        else:
            self.logger.warning(f'Failed to retrive data for artist: {self.artist}')
            print(f'Failed to retrive data for artist: {self.artist}')
        
    def _save_to_file(self, data: list):
        # Set up the directory and file path
        base_dir = r"C:\Users\wesma\OneDrive\Documents\Lyrical_Analysis\data\artists"
        os.makedirs(base_dir, exist_ok=True)
        file_path = os.path.join(base_dir, f'{self.artist}.json')

        # Save the data in JSON format
        with open(file_path, 'w', encoding='UTF-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)  # Pretty print with indent
            self.logger.info(f"Successfully wrote data to {file_path}")
    
    def _parse_albums(self, r: Response) -> list:
        dom = BeautifulSoup(r.text, 'html.parser')
        current_album = None
        albums = []

        album_divs = dom.find_all('div', {'class': 'album'})

        # Finding all the divs
        for div in album_divs:
            album_text = div.get_text(strip=True)
            
            # Check if specific album or single
            if 'album:' in album_text.lower() or 'ep:' in album_text.lower():
                # Use regex to find year in parentheses
                match = re.search(r"\((\d{4})\)", album_text)
                release_year = match.group(1) if match else None
                
                # Remove the year from the album name
                album_name = re.sub(r"\(\d{4}\)", "", album_text.split(':')[1].strip().replace('"',''))
                
                current_album = {
                    "title": album_name,
                    "songs": [],
                    "release_year": release_year
                }
                albums.append(current_album)

            elif 'other songs:' in album_text.lower():
                current_album = {
                    "title": "Singles",
                    "songs": []
                }
                albums.append(current_album)

            if current_album:
                next_div = div.find_next_sibling()
                while next_div and 'listalbum-item' in next_div.get('class', []):
                    song_link = next_div.find('a')
                    if song_link and song_link.get('href'):
                        song_title = song_link.get_text(strip=True)
                        current_album["songs"].append(song_title)
                        self.logger.info(f'Found song: {song_title} under album {current_album["title"]}')
                    else:
                        self.logger.warning(f'Song link missing for a song in {current_album["title"]}')
                    next_div = next_div.find_next_sibling()
        
        self.logger.info(f'Parsed albums: {[album["title"] for album in albums]}')
        self._save_to_file(albums)
        
