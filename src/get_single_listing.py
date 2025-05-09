import logging
import pprint
from typing import Optional, Dict
import re

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SingleListing:
    """
    A class to represent a single listing.
    """

    # Constants for selectors
    DESCRIPTION_SELECTOR = {"data-testid": "ad-description-Objektbeschreibung"}

    # Constants for next keywords
    KEYWORDS = {
        "availability_start": "Verfügbar",
        "availability_duration": "Befristung",
        "number_rooms2": "Zimmer",
        "size2": "Wohnfläche"
    }
    URL_KEY = "url"
    DESCRIPTION_KEY = "description"

    def __init__(self, url: str) -> None:
        self.url = url
        self.listing_data = {self.URL_KEY: url}
        self.soup = None

        if not self._is_valid_url(url):
            logger.error(f"Invalid URL: {url}")
            return

        try:
            self.soup = self._fetch_soup()
            self._fetch_set_single_listing_content()
        except Exception as e:
            logger.error(f"Failed to initialize SingleListing: {e}")

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """
        Validates the URL format.
        """
        return re.match(r'^https?://', url) is not None

    def _fetch_soup(self) -> BeautifulSoup:
        """
        Fetches the HTML content of a URL and returns a BeautifulSoup object.

        :return: A BeautifulSoup object of the page content.
        :raises: Exception with detailed error message if the request fails.
        """
        logger.info(f"Fetching content from {self.url}")
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except (HTTPError, ConnectionError, Timeout, RequestException) as err:
            logger.error(f"Error fetching {self.url}: {err}")
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

    def _fetch_set_single_listing_content(self) -> None:
        """
        Extracts and sets the listing details from the soup.
        """

        # Extract details next to keywords
        for key, keyword in self.KEYWORDS.items():
            self.listing_data[key] = self._get_element_next_to_string(keyword)

        # Extract description
        description_element = self.soup.find(attrs=self.DESCRIPTION_SELECTOR)
        self.listing_data["description"] = description_element.text if description_element else ""

    def get_listing_dict(self) -> Dict[str, Optional[str]]:
        """
        Returns the listing details as a dictionary.

        :return: A dictionary containing the listing details.
        """
        return self.listing_data

    def pretty_print(self) -> None:
        """
        Pretty prints the listing details in JSON format.
        """
        pprint.pprint(self.listing_data)