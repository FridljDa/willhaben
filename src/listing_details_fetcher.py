import json
import logging

import requests

from src.single_listing import SingleListing

# Constants for extracting JSON data
NEXT_DATA_START = '<script id="__NEXT_DATA__" type="application/json">'
NEXT_DATA_END = '</script>'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#TODO make this a dictionary, key value what is should be translated to
RELEVANT_CONCATENATED_KEYS_READABLE_KEYS = {
        "Verfügbar": "Verfügbar",
        'location': 'location',
        'postcode': 'postcode',
        'description' : 'description',
        'heading' : 'heading',
        'body_dyn' : 'body_dyn',
        'price' : 'price',
        'size' : 'size',
        "orgname" : "orgname",
        "floor" : "floor",
        "number_of_rooms" : "number_of_rooms",
        "rent/per_month_lettings" : 'rent_per_month_lettings',
        "address" : "address",
        'url': 'url'
}

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

    #def __init__(self, single_listing: SingleListing) -> None:
   #     self.single_listing = single_listing
    @staticmethod
    def _extract_json_data(html_content: str) -> str:
        """
        Extracts JSON data from the HTML content.

        :param html_content: The HTML content as a string.
        :return: The extracted JSON data as a string.
        """
        try:
            start_index = html_content.find(NEXT_DATA_START) + len(NEXT_DATA_START)
            end_index = html_content.find(NEXT_DATA_END, start_index)
            return html_content[start_index:end_index]
        except ValueError:
            logger.error("Failed to locate JSON data in the HTML content.")
            return ""

    @staticmethod
    def fetch_and_set_single_listing_content(single_listing: SingleListing) -> None:
        """
        Extracts and sets the listing details from the soup.
        """
        url = single_listing.listing_data['url']

        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Extract the JSON data from the <script> tag
        #TODO move ListingsOverviewFetcher._extract_json_data to a utility class
        json_data = ListingDetailsFetcher._extract_json_data(html_content)
        if not json_data:
            logger.error("Failed to extract JSON data from the HTML content.")

        parsed_data = json.loads(json_data)

        single_listing.listing_data['Befristung'] = parsed_data['props']['pageProps']['advertDetails']['advertisingParameters']['Befristung']
