import unittest
import sys
import os

from single_listing import SingleListing

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from listing_details_fetcher import ListingDetailsFetcher


class TestSingleListing(unittest.TestCase):
    def test_should_return_results(self):
        url_test = "https://www.willhaben.at/iad/immobilien/d/mietwohnungen/wien/wien-1030-landstrasse/provisionsfreie-moeblierte-wohnung-mit-perfekter-oeffentlicher-anbindung-in-1030-2007459668"
        single_listing = SingleListing(url_test)
        ListingDetailsFetcher(single_listing).fetch_and_set_single_listing_content()

        res = single_listing.get_listing_dict()
        self.assertNotEqual(len(res), 0, "Length of result should not be 0")

        # Pretty print the result
        single_listing.pretty_print()

if __name__ == '__main__':
    unittest.main()