import logging
from typing import Optional

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from bs4 import BeautifulSoup

from single_listing import SingleListing

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

        try:
            self.soup = self._fetch_soup()
        except Exception as e:
            logger.error(f"Failed to initialize SingleListing: {e}")

    def _fetch_soup(self) -> BeautifulSoup:
        """
        Fetches the HTML content of a URL and returns a BeautifulSoup object.

        :return: A BeautifulSoup object of the page content.
        :raises: Exception with detailed error message if the request fails.
        """
        logger.info(f"Fetching content from {self.single_listing.url}")
        try:
            response = requests.get(self.single_listing.url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except (HTTPError, ConnectionError, Timeout, RequestException) as err:
            logger.error(f"Error fetching {self.single_listing.url}: {err}")
            raise

    def _get_element_next_to_string(self, string_find: str) -> Optional[str]:
        """
        Extracts the text of the element next to a given string in the soup.

        :param string_find: The string to search for in the soup.
        :return: The text of the next element, or None if not found.
        """
        element = self.soup.find(string=string_find)
        if not element:
            logger.debug(f"Element with string '{string_find}' not found.")
            return None
        next_element = element.find_next()
        return next_element.text.strip() if next_element else None


    def fetch_and_set_single_listing_content(self) -> None:
        """
        Extracts and sets the listing details from the soup.
        """

        # Extract details next to keywords
        for key, keyword in self.KEYWORDS.items():
            self.add_key_value_pair(keyword, self._get_element_next_to_string(keyword))

        # Extract description
        description_element = self.soup.find(attrs=self.DESCRIPTION_SELECTOR)
        self.add_key_value_pair("description",
                                description_element.text if description_element else "")
