import json
import logging
import re  # Added for regex substitution
from pathlib import Path
from urllib.parse import urlparse

import requests

from listing.fetcher.fetcher import Fetcher
from listing.structure.multiple_listings import MultipleListings
from listing.structure.single_listing import SingleListing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for extracting JSON data
NEXT_DATA_START = '<script id="__NEXT_DATA__" type="application/json">'
NEXT_DATA_END = '</script>'

# Constants for JSON keys
KEY_PROPS = 'props'
KEY_PAGE_PROPS = 'pageProps'
KEY_SEARCH_RESULT = 'searchResult'
KEY_LISTING_SUMMARY_LIST = 'advertSummaryList'
KEY_LISTING_SUMMARY = 'advertSummary'

class ListingsOverviewFetcher:
    """
    Fetches and processes listings from a given URL.
    """

    def __init__(self, url: str, multiple_listings: MultipleListings):
        """
        Initializes the fetcher with a URL and a MultipleListings instance.

        :param url: The URL to fetch listings from.
        :param multiple_listings: An instance of MultipleListings to store the processed listings.
        """
        # Replace &rows=<some number>& in the URL with &rows=1000&
        self.url = re.sub(r"&rows=\d+&", "&rows=1000&", url)
        self.multiple_listings = multiple_listings


    def fetch_all_listings(self):
        """
        Fetches and processes listings from the URL.

        :return: A list of dictionaries containing the listings.
        """
        logger.info(f"Fetching content from {self.url}")

        try:
            # Fetch the HTML content of the URL
            html_content = Fetcher.fetch_html2(self.url)

            # Extract the JSON data from the <script> tag
            json_data = Fetcher.extract_json_data_str(html_content)
            if not json_data:
                logger.error("Failed to extract JSON data from the HTML content.")

            parsed_data = json.loads(json_data)

            # Validate and extract listings
            listings_summary = self._extract_listings_summary(parsed_data)
            if not listings_summary:
                logger.error("No listing summaries found in the JSON data.")

            # Process each listing
            for single_listing_before_conversion in listings_summary:
                self._process_single_listing(single_listing_before_conversion)

            logger.info(f"Successfully fetched and processed {len(listings_summary)} listings.")

        except requests.RequestException as req_err:
            logger.exception(f"HTTP error occurred while fetching listings: {req_err}")
        except json.JSONDecodeError as json_err:
            logger.exception(f"JSON parsing error: {json_err}")
        except KeyError as key_err:
            logger.exception(f"Missing expected key in JSON data: {key_err}")
        except Exception as e:            logger.exception(f"An unexpected error occurred: {e}")


    @staticmethod
    def _extract_listings_summary(parsed_data: dict) -> list[dict]:
        """
        Extracts listing summaries from the parsed JSON data.

        :param parsed_data: The parsed JSON data.
        :return: A list of listing summaries.
        """
        try:
            return parsed_data[KEY_PROPS][KEY_PAGE_PROPS][KEY_SEARCH_RESULT][KEY_LISTING_SUMMARY_LIST][KEY_LISTING_SUMMARY]
        except KeyError:
            logger.error("Failed to extract listing summaries due to missing keys.")
            return []

    def _process_single_listing(self, single_listing_before_conversion: dict) -> None:
        # TODO replace by fetcher._process_single_listing
        """
        Processes a single listing and appends it to the multiple listings.

        :param single_listing_before_conversion: The raw listing data before conversion.
        """
        single_listing = SingleListing()
        seo_url = single_listing_before_conversion['attributes']['attribute'][19]['values'][0]
        if seo_url.startswith('immobilien/'):
            url = 'https://www.willhaben.at/iad/' + seo_url
            single_listing.add_key_value_pair('url', url)
            self.multiple_listings.append_listing(single_listing)
