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
            start_index = html_content.find(NEXT_DATA_START) + len(NEXT_DATA_START)
            end_index = html_content.find(NEXT_DATA_END, start_index)
            json_data = html_content[start_index:end_index]
            parsed_data = json.loads(json_data)

            # Extract and process the listings
            advert_summaries = parsed_data['props']['pageProps']['searchResult']['advertSummaryList']['advertSummary']
            for single_listing_before_conversion in advert_summaries:
                # Flatten the attributes into the main dictionary
                for attribute in single_listing_before_conversion['attributes']['attribute']:
                    name = attribute['name'].lower()
                    value = attribute['values'][0]
                    single_listing_before_conversion[name] = int(value) if value.isdigit() else value

                full_url = f"https://www.willhaben.at/iad/{single_listing_before_conversion['seo_url']}"

                single_listing = SingleListing(full_url)
                single_listing.update_dict(single_listing_before_conversion)

                self.multiple_listings.append_listing(single_listing)

        except Exception as e:
            logger.exception(f"An error occurred while fetching listings from {self.url}")
            return []
