from pymongo import MongoClient
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nrclex import NRCLex
import logging

# Download necessary NLTK resources for tokenization
nltk.download('punkt')

# Initiate Sentiment Analyzer
vader_analyzer = SentimentIntensityAnalyzer() # Contains txt files with scores for different character combinations

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client.lyrical_analysis_db
songs_collection = db.songs

logger = logging.getLogger(__name__)


def analyze_sentiment_vader(text):
    """ 
        Perform VADER sentiment analysis
        Gives basic scores: negative, positive, neutral, compound
    """
    return vader_analyzer.polarity_scores(text)

def analyze_sentiment_nrc(text):
    """
        Perform NRC Lexicon sentiment analysis
        Gives more specific scores
    """
    # Perform NRC analysis
    nrc = NRCLex(text)

    # Initialize emotion scores to zero
    emotion_scores = {
        "anger": 0, "anticipation": 0, "disgust": 0, "fear": 0,
        "joy": 0, "sadness": 0, "surprise": 0, "trust": 0
    }
    
    # Calculate frequency of each emotion
    total_emotions = sum(nrc.raw_emotion_scores.values())
    if total_emotions > 0:
        for emotion, score in nrc.raw_emotion_scores.items():
            if emotion in emotion_scores:
                emotion_scores[emotion] = score / total_emotions
    return emotion_scores


def update_song_with_sentiment(song):
    lyrics = song.get("lyrics", "")
    # Get VADER sentiment scores
    vader_scores = analyze_sentiment_vader(lyrics)
    # Get NRC Lexicon emotion scores
    nrc_scores = analyze_sentiment_nrc(lyrics)
    
    # Update document with sentiment information
    sentiment_data = {
        "vader": vader_scores,
        "nrc": nrc_scores
    }
    songs_collection.update_one(
        {"_id": song["_id"]},
        {"$set": {"sentiment": sentiment_data}}
    )

# Retrieve all songs and update with sentiment analysis
for song in songs_collection.find():
    update_song_with_sentiment(song)
    
"""Analyzes all of the songs listed in the collection and adds an additional section for sentiment scores"""