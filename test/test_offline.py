import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fetching.fetcher.listings_overview_fetcher import ListingsOverviewFetcher
from fetching.listings.multiple_listings import MultipleListings

import unittest


class TestWillhabenAPI(unittest.TestCase):
    def test_should_return_results(self):
        multiple_listings = MultipleListings()

        url_query = Path("test_data") / "response_content.html"

        url_query = url_query.read_text()
        lof = ListingsOverviewFetcher(url_query, multiple_listings)
        lof.fetch_all_listings()

        print(f"Number of listings: {len(multiple_listings.list_of_listings)}")

        #self.assertNotEqual(len(multiple_listings.list_of_listings), 0, "length of result is not 0")

if __name__ == '__main__':
    unittest.main()