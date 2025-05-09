import json
import logging
import requests
from multiple_listings import MultipleListings
from single_listing import SingleListing

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
KEY_ATTRIBUTES = 'attributes'
KEY_ATTRIBUTE = 'attribute'

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

    def fetch_all_listings(self):
        """
        Fetches and processes listings from the URL.

        :return: A list of dictionaries containing the listings.
        """
        logger.info(f"Fetching content from {self.url}")

        try:
            # Fetch the HTML content of the URL
            response = requests.get(self.url)
            response.raise_for_status()
            html_content = response.text

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
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")

    def _extract_json_data(self, html_content: str) -> str:
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

    def _extract_listings_summary(self, parsed_data: dict) -> list[dict]:
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

    def _process_single_listing(self, single_listing_before_conversion: dict):
        """
        Processes a single listing and appends it to the multiple listings.

        :param single_listing_before_conversion: The raw listing data before conversion.
        """
        try:
            # Flatten the attributes into the main dictionary
            for attribute in single_listing_before_conversion[KEY_ATTRIBUTES][KEY_ATTRIBUTE]:
                name = attribute['name'].lower()
                value = attribute['values'][0]
                single_listing_before_conversion[name] = int(value) if value.isdigit() else value

            full_url = f"https://www.willhaben.at/iad/{single_listing_before_conversion['seo_url']}"

            single_listing = SingleListing(full_url)
            single_listing.update_dict(single_listing_before_conversion)

            self.multiple_listings.append_listing(single_listing)
        except KeyError as key_err:
            logger.error(f"Failed to process a single listing due to missing key: {key_err}")
