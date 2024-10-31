# scripts/scrape_lyrics.py

import requests
from requests import Response
from bs4 import BeautifulSoup
import logging
import re

class AZLyrics:

    def __init__(self, artist: str, song: str): # saves artist: str, song: str as an annotation (dictionary)
        self.artist = artist
        self.song = song
        self.logger = logging.getLogger(__name__) # Creates logger object

    # methods to prep the artist and song title field to search
    def _parse_artist(self) -> str: # _ denotes for coder to treat as private method. -> str, annotates return as a string
        self.logger.info(f'Parsing artist {self.artist}')
        return re.sub(r'[^a-z0-9\s]', '', self.artist.lower().replace(' ', ''))
    
    def _parse_song(self) -> str:
        self.logger.info(f'Paring song: {self.song}')
        return re.sub(r'[^a-z0-9\s]', '', self.song.lower().replace(' ', ''))
    
    # method to prepare url to be used dynamically
    def url(self) -> str:
        url = 'https://www.azlyrics.com/lyrics/{}/{}.html'\
                .format(self._parse_artist().replace('the',''), self._parse_song())
        self.logger.info(f'Generated URL: {url}')
        return url

    # method to make an HTTP request to AZLyrics and return lyrics
    def open_url(self):
        url = self.url()
        try:
            response = requests.get(url)
            response.raise_for_status() # Raises error for bad responses
            self.logger.info(f'Successfully opened URL: {url}')
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to open URL: {url}')
            return None
        
        lyrics = album = writers = genre = None

        if response.ok: # checks for errors with the request
            lyrics = self._parse_lyrics(response)
            genre = self._parse_genre(response)
            album = self._parse_album(response)
            writers = self._parse_writers(response)
        
        self.logger.info(f'Lyrics: {lyrics}')
        self.logger.info(f'Genre: {genre}')
        self.logger.info(f'Album: {album}')
        self.logger.info(f'Writers: {writers}')

        return lyrics, genre, album, writers
    
    def _parse_genre(self, r: Response) -> str:
        dom = BeautifulSoup(r.text, 'html.parser')
        header = dom.head
        script_tag = header.find('script', text=lambda t: 'window.rtkGPTSlotsTargeting' in t)

        if script_tag:
            script_content = script_tag.string
            start_index = script_content.find('["genre", "') + len('["genre", "')
            end_index = script_content.find('"]', start_index)
            genre = script_content[start_index:end_index]
            self.logger.info(f'Genre found: {genre}')
            return genre
        self.logger.warning('Genre not found')
        return "Genre not found"

    def _parse_album(self, r: Response) -> str:
        dom = BeautifulSoup(r.text, 'html.parser')
        album_div = dom.find('div', class_='songinalbum_title')
        if album_div:
            album = album_div.get_text(strip=True)
            album = album.replace('album:', '').strip()
            self.logger.info(f'Album found: {album}')
            return album
        self.logger.warning(f'Album not found')
        return "Album not found"
    
    def _parse_writers(self, r: Response) -> str:
        dom = BeautifulSoup(r.text, 'html.parser')
        smt_divs = dom.find_all('div', class_='smt')

        for div in smt_divs:
            small_tag = div.find('small')
            if small_tag and 'Writer(s):' in small_tag.get_text(strip=True):
                writers = small_tag.get_text(strip=True).replace('Writer(s):','').strip()
                self.logger.info(f'Writer(s) found: {writers}')
                return writers
            
        self.logger.warning(f'Writers not found')
        return "Writers not found"    
    
    # method to isolate the lyrics from the rest of the html file
    def _parse_lyrics(self, r: Response) -> str:
        dom = BeautifulSoup(r.text, 'html.parser') # DOM stands for Document Object Model
        body = dom.body # body section of the html file
        
        divs = body.find_all('div', {'class': 'col-xs-12 col-lg-8 text-center'})[0]

        target = {0: 0}

        for i, d in enumerate(divs):
            try:
                query = d.find_all('br')
                n_br = len(query)
                if n_br > list(target.values())[0]:
                    target = {i: n_br}
            except Exception as e:
                self.logger.error(f'Error parsing div at index {i}: {e}')

        target = list(target.keys())[0]
        lyrics = list(divs.children)[target].text

        self.logger.info('Lyrics successfully parsed')
        return lyrics
    
    