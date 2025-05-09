import unittest
from src.listings_overview_fetcher import fetch_all_listings

class TestWillhabenAPI(unittest.TestCase):
    def test_should_return_results(self):
        url = 'https://willhaben.at/iad/kaufen-und-verkaufen/marktplatz/pc-komponenten-5878'
        listings = fetch_all_listings(url)
        self.assertNotEqual(len(listings), 0, "length of result is not 0")

if __name__ == '__main__':
    unittest.main()