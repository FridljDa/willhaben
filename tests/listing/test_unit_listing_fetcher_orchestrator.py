import unittest
from unittest.mock import patch, MagicMock
from listing.listing_fetcher_orchestrator import ListingFetcherOrchestrator
from listing.structure.multiple_listings import ListingRepository

class TestListingFetcherOrchestrator(unittest.TestCase):
    @patch('listing.listing_fetcher_orchestrator.ListingsOverviewFetcher')
    @patch('listing.listing_fetcher_orchestrator.ListingDetailsFetcher')
    @patch('listing.listing_fetcher_orchestrator.ListingRepository')
    def test_fetch_and_process_listings(self, MockListingRepository, MockListingDetailsFetcher, MockListingsOverviewFetcher):
        # Arrange
        url_query = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=1000&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40'
        mock_multiple_listings = MockListingRepository.return_value
        mock_multiple_listings.list_of_listings = [MagicMock(), MagicMock()]

        orchestrator = ListingFetcherOrchestrator(url_query, silent=False)

        # Act
        orchestrator.fetch_and_process_listings()

        # Assert
        MockListingsOverviewFetcher.assert_called_once_with(url_query, mock_multiple_listings)
        MockListingsOverviewFetcher.return_value.fetch_all_listings.assert_called_once()

        mock_multiple_listings.apply_function_to_each_listing.assert_called_once()
        mock_multiple_listings.select_listing_keys_and.assert_called_once()
        mock_multiple_listings.pretty_print.assert_called_once()
        self.assertEqual(len(mock_multiple_listings.list_of_listings), 2)

if __name__ == '__main__':
    unittest.main()