import unittest
from pathlib import Path

from listing.fetcher.fetcher import Fetcher
from listing.listing_fetcher_orchestrator import ListingFetcherOrchestrator
from project_root import PROJECT_ROOT

path_multiple_listings_csv = PROJECT_ROOT / "test" / "test_data" / "listings.csv"
path_offline_html = Path(PROJECT_ROOT) / "test" / "test_data" / "response_content.html"
url_query_test = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=1000&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40'

class TestListingFetcherOrchestratorEndToEnd(unittest.TestCase):

    def setUp(self):
        # Clean up the CSV file before each test
        if path_multiple_listings_csv.exists():
            path_multiple_listings_csv.unlink()

    def tearDown(self):
        # Clean up the CSV file after each test
        if path_multiple_listings_csv.exists():
            path_multiple_listings_csv.unlink()

    def test_fetch_and_process_listings_end_to_end(self):
        # Arrange
        orchestrator = ListingFetcherOrchestrator(url_query_test, 
                                                  path=path_multiple_listings_csv, 
                                                  silent=False)

        # Act
        orchestrator.fetch_and_process_listings()

        # Assert
        self.assertGreater(len(orchestrator.multiple_listings.list_of_listings), 0)
        self.assertIs(path_multiple_listings_csv.exists(), True)
        self.assertGreater(path_multiple_listings_csv.stat().st_size, 0)

    def test_fetch_and_process_listings_end_to_end_offline(self):
        # Arrange
        orchestrator = ListingFetcherOrchestrator(path_offline_html,
                                                  path=path_multiple_listings_csv,
                                                  silent=False)

        # Act
        orchestrator.fetch_and_process_listings()

        # Assert
        self.assertGreater(len(orchestrator.multiple_listings.list_of_listings), 0)
        self.assertIs(path_multiple_listings_csv.exists(), True)
        self.assertGreater(path_multiple_listings_csv.stat().st_size, 0)

if __name__ == '__main__':
    if not path_offline_html.exists():
        print(f"Offline HTML file not found at {path_offline_html}. Please fetch it first.")
        fetcher = Fetcher(url_query_test)
        html_content = fetcher.fetch_html()
        path_offline_html.parent.mkdir(parents=True, exist_ok=True)
        path_offline_html.write_text(html_content, encoding='utf-8')

    unittest.main()
