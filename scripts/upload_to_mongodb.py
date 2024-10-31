# scripts/upload_to_mongodb.py

from pymongo import MongoClient
import os
from scripts.scrape_lyrics import AZLyrics
import json
import logging
import time
import random

def random_delay(min_delay=3, max_delay=15):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

# TODO: When script ran, the artist name was added, but the Albums array was empty

logger = logging.getLogger(__name__)
# Connect to MongoDB Client
client = MongoClient("mongodb://localhost:27017/")

# MongoDB operates on a lazy creation model, which will only connect
# if the database doesn't exist already

# Connect to database called "lyrical_analysis_db"
db = client.lyrical_analysis_db

# Connect to collections within the database
artists_collection = db.artists
songs_collection = db.songs
albums_collection = db.albums

def add_artist_to_db(artist_file, num_albums:int = None, album_title: str = None):
    """
    Adds an artist, albums, and songs to the MongoDB collections from a file.
    :param artist_file: Path to the artist's file containing album and song info.
    :param num_albums: Optionally limit to the top n albums.
    :param album_title: Optionally specify a single album to add.
    """

    # Load artist data from input file
    artist_name = os.path.basename(artist_file).replace('.json','')

    with open(artist_file, 'r', encoding='utf-8') as f:
        artist_data = json.load(f)

    albums_to_add = []
    
    # If album_title is provided, only add that album
    if album_title:
        logger.info("Album: {album_title} provided.")
        albums_to_add = [album for album in artist_data if album['title'] == album_title]
        if not albums_to_add:
            logger.error(f"ERROR: Album '{album_title}' not found for {artist_name}.")
            return
    else:
        albums_to_add = artist_data[:num_albums] if num_albums else artist_data
        logger.info(f"Adding top {num_albums if num_albums else 'all'} albums from {artist_name}'s discography.")

        # Add artist to DB if not already present
    if not artists_collection.find_one({'name': artist_name}):
        artist_doc = {
            'name': artist_name,
            'albums': [album['title'] for album in albums_to_add]
        }
        artists_collection.insert_one(artist_doc)

    # Loop through albums and add them to the 'albums' collection
    for album in albums_to_add:
        album_title = album['title']
        release_year = album.get('release_year', 'Unknown')  # Extract release year if available
        
        # Add album to MongoDB if not already present
        if not albums_collection.find_one({'title': album_title, 'artist': artist_name}):
            album_doc = {
                'title': album_title,
                'artist': artist_name,
                'release_year': release_year,
                'songs': album.get('songs', [])
            }
            albums_collection.insert_one(album_doc)

        # Loop through songs in the album and add them to the 'songs' collection
        for song in album.get('songs', []):
            try:
                if not songs_collection.find_one({'title': song, 'artist': artist_name}):
                    random_delay() # Randomizes the requests so that less chance of website blocking IP
                    # Use the AZLyrics class to scrape extra info if needed (e.g., lyrics, genre)
                    azlyrics = AZLyrics(artist=artist_name, song=song)
                    lyrics, genre, _, writers = azlyrics.open_url()

                    song_doc = {
                        'title': song,
                        'artist': artist_name,
                        'album': album_title,
                        'release_year': release_year,
                        'lyrics': lyrics,
                        'genre': genre,
                        'writers': writers
                    }
                    songs_collection.insert_one(song_doc)
            except Exception as e:
                logger.error(f"An error occurred while processing the song '{song}': {e}")
                print(f"Skipping song '{song}' due to an error.")

    print(f"Successfully added {artist_name} to MongoDB.")
