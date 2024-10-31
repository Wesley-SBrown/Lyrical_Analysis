# scripts/bulk_scrape_lyrics

import os
import logging

class BulkScraper:
    """ Used to skip over saving the discography to a file. 
        Immediatly does every song. 
        TODO: Utilize the existing functions to scraping and save in one run."""
    def __init__(self, artist: str):
        self.artist = artist
        self.logger = logging.getLogger(__name__)

    
