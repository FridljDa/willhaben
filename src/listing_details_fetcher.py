import logging

from src.single_listing import SingleListing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListingDetailsFetcher:

    # Constants for selectors
    DESCRIPTION_SELECTOR = {"data-testid": "ad-description-Objektbeschreibung"}

    # Constants for next keywords
    KEYWORDS = {
        "availability_start": "Verfügbar",
        "availability_duration": "Befristung",
        "number_rooms2": "Zimmer",
        "size2": "Wohnfläche"
    }

    DESCRIPTION_KEY = "description"

    def __init__(self, single_listing: SingleListing) -> None:
        self.single_listing = single_listing

    def fetch_and_set_single_listing_content(self) -> None:
        """
        Extracts and sets the listing details from the soup.
        """

        #parsed_data['props']['pageProps']['advertDetails']['advertisingParameters']['Befristung']
