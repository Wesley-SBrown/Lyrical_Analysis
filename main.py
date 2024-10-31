# main.py

import argparse
import logging
from datetime import datetime
from scripts.scrape_lyrics import AZLyrics
from scripts.scrape_discography import AZArtists
from scripts.upload_to_mongodb import add_artist_to_db
import os

# Logging setup
log_filename = f'logs/scraping_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    filename=log_filename,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def retrieve_discography(artist_name):
    discography_request = AZArtists(artist=artist_name)
    discography_request.open_url()

def retrieve_song(artist_name, song_title):
    lyrics_request = AZLyrics(artist=artist_name, song=song_title)
    lyrics, genre, album, writers = lyrics_request.open_url()
    print(lyrics, genre, album, writers, sep='\n')

def upload_artist_to_mongodb(artist_file, num_albums=None, album_title=None):
    # Upload artist's discography and song data to MongoDB.
    add_artist_to_db(artist_file, num_albums=num_albums, album_title=album_title)
    artist_name = os.path.basename(artist_file).replace('.json','')
    print(f"Artist {artist_name} data uploaded to MongoDB.")

def list_commands():
    print("Available commands:")
    print("1) discography: Retrieve an artist's discography")
    print("2) song: Retrieve lyrics for a specific song")
    print("3) upload: Upload artist data to MongoDB")
    print("4) list: List all available commands")

if __name__ == '__main__':
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="AZLyrics Scraper CLI")

    # Subcommands for different tasks
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommand for retrieving discography
    parser_discography = subparsers.add_parser('discography', help="Retrieve an artist's discography")
    parser_discography.add_argument('artist', type=str, help="Artist's name")

    # Subcommand for retrieving a specific song
    parser_song = subparsers.add_parser('song', help="Retrieve lyrics for a specific song")
    parser_song.add_argument('artist', type=str, help="Artist's name")
    parser_song.add_argument('song', type=str, help="Song title")

    # Subcommand for uploading artist data to MongoDB
    parser_upload = subparsers.add_parser('upload', help="Upload artist data to MongoDB")
    parser_upload.add_argument('--file', type=str, required=True, help="Path to the artist's JSON file")
    parser_upload.add_argument('--num_albums', type=int, help="Limit to the top N albums")
    parser_upload.add_argument('--album_title', type=str, help="Upload data for a specific album")

    # Subcommand for listing all commands
    parser_list = subparsers.add_parser('list', help="List all available commands")

    # Parse the command-line arguments
    args = parser.parse_args()

    try:
        if args.command == 'discography':
            retrieve_discography(args.artist)
        elif args.command == 'song':
            retrieve_song(args.artist, args.song)
        elif args.command == 'upload':
            if not os.path.exists(args.file):
                print(f"The file {args.file} does not exist.")
            else:
                upload_artist_to_mongodb(args.file, num_albums=args.num_albums, album_title=args.album_title)
        elif args.command == 'list':
            list_commands()
        else:
            print("Invalid command. Use --help for more details.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print("An error occurred. Please check the logs for more details.")
