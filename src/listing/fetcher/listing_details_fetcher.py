import logging

from listing.fetcher.fetcher import Fetcher
from listing.structure.single_listing import SingleListing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListingDetailsFetcher(Fetcher):
    """
    Fetches and processes details for a single listing.
    """

    def __init__(self, url: str):
        """
        Initializes the fetcher with a URL.
        """
        super().__init__(url)  # Initialize the parent class

    @staticmethod
    def fetch_and_set_single_listing_content(single_listing: SingleListing) -> None:
        """
        Extracts and sets the listing details from the soup.
        """
        url = single_listing.listing_data['url']
        parsed_data = Fetcher.fetch_content_as_json(url)  # Use inherited method

        listing_attribute = parsed_data['props']['pageProps']['advertDetails']['attributes']['attribute']
        for listing_attribute_key_value in listing_attribute:
            single_listing.listing_data[listing_attribute_key_value["name"]] = listing_attribute_key_value["values"]

