# Lyrical Analysis Project

This project focuses on analyzing song lyrics from AZLyrics by scraping, processing, and performing advanced analysis to gain insights. It is designed to showcase data science, natural language processing (NLP), and software engineering skills.

## Features

### 1. Data Collection
- **Scraping:** Lyrics and metadata (albums, artists) are scraped from AZLyrics using Python scripts.
- **Storage:** Data is stored in JSON files in the `data/artists` folder.

### 2. Data Processing
- **Preprocessing:** Handles raw lyric data for tasks like cleaning, tokenization, and sentiment analysis.
- **Storage in MongoDB:** The `upload_to_mongodb.py` script uploads artist, album, and song data into a MongoDB database for scalable storage.

### 3. Sentiment Analysis
- Uses **VADER Sentiment Analysis** to calculate:
  - Negative, Neutral, Positive, and Compound scores.
- Leverages the **NRC Lexicon** to detect emotions like joy, anger, and sadness in lyrics.

### 4. Embedding Generation
- Creates vector embeddings of song lyrics for:
  - Similarity analysis.
  - Clustering and advanced modeling.

### 5. Exploratory Data Analysis (EDA)
- Includes Jupyter Notebooks for:
  - Visualizing trends in lyrics.
  - Insights into artist-specific themes and sentiments.

### 6. CLI Interaction
- The project includes a command-line interface for:
  - Running scraping scripts.
  - Uploading data to MongoDB.
  - Analyzing lyrics and generating embeddings.

## Directory Structure
```
Lyrical_Analysis/
├── config/                  # Configuration files
├── data/                    # Scraped and processed data
│   ├── artists/             # JSON files for each artist
│   ├── embeddings/          # Generated embeddings
│   └── processed/           # Intermediate processed data
├── logs/                    # Logging files
├── notebooks/               # Jupyter Notebooks for EDA
├── scripts/                 # Python scripts for scraping and analysis
│   ├── bulk_scrape_lyrics.py
│   ├── generate_embeddings.py
│   ├── scrape_discography.py
│   ├── scrape_lyrics.py
│   ├── sentiment_analysis.py
│   └── upload_to_mongodb.py
├── tests/                   # Unit tests
│   └── test_scraping.py
├── venv/                    # Virtual environment
├── main.py                  # Main entry point for CLI
└── requirements.txt         # Python dependencies
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Wesley-SBrown/Lyrical_Analysis.git
   cd Lyrical_Analysis
   ```

2. **Set up a virtual environment:**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate    # For Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB:**
   - Install and run a MongoDB instance locally or connect to a remote instance.
   - Update the connection string in `config/settings.py`.

## Usage

### Scrape Lyrics
Run the scraper for a specific artist:
```bash
python scripts/scrape_discography.py "Artist Name"
```

### Upload Data to MongoDB
Add scraped data to the database:
```bash
python scripts/upload_to_mongodb.py "path/to/artist.json"
```

### Perform Sentiment Analysis
Analyze sentiment of lyrics:
```bash
python scripts/sentiment_analysis.py
```

## Contributing
Feel free to fork this project, submit issues, or make pull requests to improve the project.

## License
This project is licensed under the MIT License.
