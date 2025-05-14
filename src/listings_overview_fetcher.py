import json
import logging
from pathlib import Path
from urllib.parse import urlparse

import requests

from listing_details_fetcher import ListingDetailsFetcher
from src.multiple_listings import MultipleListings
from src.single_listing import SingleListing

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
        self.url = url
        self.multiple_listings = multiple_listings

    @staticmethod
    def fetch_html(url_path: str) -> str:
        parsed = urlparse(url_path)
        if parsed.scheme in ("http", "https"):
            # It's a URL
            response = requests.get(url_path)
            response.raise_for_status()
            return response.text
        else:
            # It's a local file path
            file_path = Path(url_path)
            return file_path.read_text(encoding="utf-8")


    def fetch_all_listings(self):
        """
        Fetches and processes listings from the URL.

        :return: A list of dictionaries containing the listings.
        """
        logger.info(f"Fetching content from {self.url}")

        try:
            # Fetch the HTML content of the URL
            html_content = self.fetch_html(self.url)

            print(html_content)
            # Extract the JSON data from the <script> tag
            json_data = self._extract_json_data(html_content)
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

    @staticmethod
    def _flatten_nested_dict(nested_dict: dict, parent_key="", sep="_") -> dict:
        items = []
        for k, v in nested_dict.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(
                    ListingsOverviewFetcher._flatten_nested_dict(v, new_key,
                                                                 sep).items())
            else:
                items.append((new_key, v))
        return dict(items)



    def _process_single_listing(self, single_listing_before_conversion: dict) -> SingleListing:
        """
        Processes a single listing and appends it to the multiple listings.

        :param single_listing_before_conversion: The raw listing data before conversion.
        """
        single_listing = SingleListing()
        url = 'https://www.willhaben.at/iad/' + single_listing_before_conversion['attributes']['attribute'][19]['values'][0]#['values']
        single_listing.add_key_value_pair('url', url)

        ListingDetailsFetcher.fetch_and_set_single_listing_content(single_listing)
        #TODO fetch the details of the listing
        self.multiple_listings.append_listing(single_listing)
        return single_listing