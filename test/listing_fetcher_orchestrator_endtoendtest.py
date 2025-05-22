import unittest
from pathlib import Path

from listing.listing_fetcher_orchestrator import ListingFetcherOrchestrator


class TestListingFetcherOrchestratorEndToEnd(unittest.TestCase):
    def test_fetch_and_process_listings_end_to_end(self):
        # Arrange
        url_query_test = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=1000&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40'
        orchestrator = ListingFetcherOrchestrator(url_query_test, silent=False)

        # Act
        orchestrator.fetch_and_process_listings()

        # Assert
        self.assertGreater(len(orchestrator.multiple_listings.list_of_listings), 0)

    def test_fetch_and_process_listings_end_to_end_offline(self):
        # Arrange
        path_html = Path("test_data") / "response_content.html"
        path_html_string = path_html.read_text()

        orchestrator = ListingFetcherOrchestrator(path_html_string, silent=False)

        # Act
        orchestrator.fetch_and_process_listings()

        # Assert
        self.assertGreater(len(orchestrator.multiple_listings.list_of_listings), 0)

if __name__ == '__main__':
    unittest.main()