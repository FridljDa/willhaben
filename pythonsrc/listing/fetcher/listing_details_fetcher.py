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

  def __init__(self, single_listing_with_url: SingleListing):
    """
    Initializes the fetcher with a URL.
    """
    super().__init__(single_listing_with_url.listing_data[
                       'url'])  # Initialize the parent class
    self.single_listing = single_listing_with_url

  def fetch_and_set_single_listing_content(self) -> None:
    """
    Extracts and sets the listing details from the soup.
    """
    parsed_data = self.fetch_content_as_json()

    listing_attribute = \
      parsed_data['props']['pageProps']['advertDetails']['attributes'][
        'attribute']
    for listing_attribute_key_value in listing_attribute:
      values = listing_attribute_key_value["values"][0]
      self.single_listing.listing_data[
        listing_attribute_key_value["name"]] = values
