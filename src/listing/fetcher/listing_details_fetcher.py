import logging

from listing.fetcher.fetcher import Fetcher
from listing.structure.single_listing import SingleListing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListingDetailsFetcher:

    @staticmethod
    def fetch_and_set_single_listing_content(single_listing: SingleListing) -> None:
        """
        Extracts and sets the listing details from the soup.
        """
        url = single_listing.listing_data['url']
        parsed_data = Fetcher.fetch_json_from_url(url)

        listing_attribute = parsed_data['props']['pageProps']['advertDetails']['attributes']['attribute']
        for listing_attribute_key_value in listing_attribute:
          single_listing.listing_data[listing_attribute_key_value["name"]] = listing_attribute_key_value["values"]

