import unittest
from scripts.scrape_lyrics import AZLyrics

class TestAZLyrics(unittest.TestCase):

    def setUp(self):
        # Setup runs before each test case
        self.az = AZLyrics(artist='All Time Low', song='The Other Side')

    def test_parse_artist(self):
        # Test artist parsing
        self.assertEqual(self.az._parse_artist(), 'alltimelow')

    def test_parse_song(self):
        # Test song parsing
        self.assertEqual(self.az._parse_song(), 'theotherside')

    def test_url(self):
        # Test URL generation
        expected_url = 'https://www.azlyrics.com/lyrics/alltimelow/theotherside.html'
        self.assertEqual(self.az.url(), expected_url)

    def test_open_url(self):
        # Test if the lyrics and genre are correctly scraped
        lyrics, genre, album, writers = self.az.open_url()
        self.assertIsNotNone(lyrics)
        self.assertIsNotNone(genre)
        self.assertIsNotNone(album)
        self.assertIsNotNone(writers)
        self.assertIn('On the other side', lyrics)  # Check a phrase in the lyrics
        self.assertEqual(genre, 'Pop')
        self.assertEqual(album, """Tell Me I'm Alive"(2023)""")
        self.assertEqual(writers,'Bonnie Leigh McKee, Zakk Cervini, Jack Barakat, Alex Gaskarth')

if __name__ == '__main__':
    unittest.main()
