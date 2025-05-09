import unittest
from src.get_listings import fetch_all_listings
from src.get_single_listing import SingleListing


class TestSingleListing(unittest.TestCase):
    def test_should_return_results(self):
        url_test = "https://www.willhaben.at/iad/immobilien/d/mietwohnungen/wien/wien-1030-landstrasse/provisionsfreie-moeblierte-wohnung-mit-perfekter-oeffentlicher-anbindung-in-1030-2007459668"
        res = (SingleListing(url_test).get_listing_dict())
        self.assertNotEqual(len(res), 0, "length of result is not 0")

        print("res")
        print(res)

if __name__ == '__main__':
    unittest.main()