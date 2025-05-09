import json
import logging

import requests

from multiple_listings import MultipleListings
from single_listing import SingleListing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListingsOverviewFetcher:
    """
    Fetches listings from a given URL and processes the data.
    """

    def __init__(self, url, multiple_listings: MultipleListings):
        self.url = url
        self.multiple_listings = multiple_listings

    def fetch_all_listings(self):
        """
        Gets the listings from a URL.

        :return: A list of dictionaries containing the listings.
        """
        logger.info(f"Fetching content from {self.url}")

        try:
            # Fetch the HTML content of the URL
            response = requests.get(self.url)
            response.raise_for_status()
            html_content = response.text

            # Extract the JSON data from the <script> tag
            start_marker = '<script id="__NEXT_DATA__" type="application/json">'
            end_marker = '</script>'
            start_index = html_content.find(start_marker) + len(start_marker)
            end_index = html_content.find(end_marker, start_index)
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

                full_url = 'https://www.willhaben.at/iad/' + single_listing_before_conversion['seo_url']

                single_listing = SingleListing(full_url)

                single_listing.update_dict(single_listing_before_conversion)

                self.multiple_listings.append_listing(single_listing)


        except Exception as e:
            print(f"An error occurred: {e}")
            return []
