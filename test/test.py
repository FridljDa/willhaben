import unittest
from src.listings_overview_fetcher import ListingsOverviewFetcher
from src.multiple_listings import MultipleListings


class TestWillhabenAPI(unittest.TestCase):
    def test_should_return_results(self):
        multiple_listings = MultipleListings()

        url_query = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=30&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40'

        ListingsOverviewFetcher(url_query, multiple_listings).fetch_all_listings()

        print(f"Number of listings: {len(multiple_listings.list_of_listings)}")

        self.assertNotEqual(len(multiple_listings.list_of_listings), 0, "length of result is not 0")

if __name__ == '__main__':
    unittest.main()