import unittest
from pathlib import Path

from listing.fetcher.fetcher import Fetcher
from listing.listing_fetcher_orchestrator import ListingFetcherOrchestrator


class TestListingFetcherOrchestratorEndToEnd(unittest.TestCase):
    path_offline_html = Path("test_data") / "response_content.html"
    url_query_test = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=1000&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40'

    def test_fetch_and_process_listings_end_to_end(self):
        # Arrange
        orchestrator = ListingFetcherOrchestrator(self.url_query_test, silent=False)

        # Act
        orchestrator.fetch_and_process_listings()

        # Assert
        self.assertGreater(len(orchestrator.multiple_listings.list_of_listings), 0)

    def download_html(self):
        fetcher = Fetcher(self.url_query_test)
        html_content = fetcher.fetch_html()
        with open(self.path_offline_html, 'w', encoding='utf-8') as file:
            file.write(html_content)

    def test_fetch_and_process_listings_end_to_end_offline(self):
        # Arrange
        orchestrator = ListingFetcherOrchestrator(self.path_offline_html, silent=False)

        # Act
        orchestrator.fetch_and_process_listings()

        # Assert
        self.assertGreater(len(orchestrator.multiple_listings.list_of_listings), 0)

if __name__ == '__main__':
    #unittest.main()
    endendtester = TestListingFetcherOrchestratorEndToEnd()
    endendtester.download_html()