import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.listings_overview_fetcher import ListingsOverviewFetcher
from src.multiple_listings import MultipleListings

import unittest


class TestWillhabenAPI(unittest.TestCase):
    def test_should_return_results(self):
        multiple_listings = MultipleListings()

        url_query = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=30&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40'
        #url_query = 'https://www.willhaben.at/iad/immobilien/d/mietwohnungen/wien/wien-1020-leopoldstadt/top-lage-2-zimmer-wohnung-u1-nestroyplatz-1587913155'
        ListingsOverviewFetcher(url_query, multiple_listings).fetch_all_listings()

        print(f"Number of listings: {len(multiple_listings.list_of_listings)}")

        self.assertNotEqual(len(multiple_listings.list_of_listings), 0, "length of result is not 0")

if __name__ == '__main__':
    unittest.main()