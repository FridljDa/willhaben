import json
import logging
from typing import Optional, Dict

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
        "number_rooms": "Zimmer",
        "size2": "Wohnfläche"
    }

    def __init__(self, url: str) -> None:
        self.url = url

        self.listing_data = {
            "url": url
        }

        try:
            self.soup = self._fetch_soup()
            self._fetch_set_single_listing_content()
        except Exception as e:
            logger.error(f"Failed to initialize SingleListing: {e}")
            self.soup = None

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
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise Exception(
                f"HTTP error occurred while fetching {self.url}: {http_err}")
        except ConnectionError as conn_err:
            logger.error(f"Connection error occurred: {conn_err}")
            raise Exception(
                f"Connection error occurred while fetching {self.url}: {conn_err}")
        except Timeout as timeout_err:
            logger.error(f"Request timed out: {timeout_err}")
            raise Exception(f"Request to {self.url} timed out: {timeout_err}")
        except RequestException as req_err:
            logger.error(f"An error occurred during the request: {req_err}")
            raise Exception(
                f"An error occurred while fetching {self.url}: {req_err}")

    def _get_element_next_to_string(self, string_find: str) -> Optional[str]:
        """
        Extracts the text of the element next to a given string in the soup.

        :param string_find: The string to search for in the soup.
        :return: The text of the next element, or None if not found.
        """
        element = self.soup.find(string=string_find)
        if element is None:
            logger.warning(f"Element with string '{string_find}' not found in the HTML content.")
            return None
        next_element = element.find_next()
        return next_element.text if next_element else None

    def _fetch_set_single_listing_content(self) -> None:
        """
        Extracts and sets the listing details from the soup.
        """
        # Extract wh_code from the URL
        self.listing_data["wh_code"] = "".join(reversed([char for char in self.url[::-1] if
                                         char.isnumeric() or char == "-"])).split(
            "-")[0]

        # Extract details next to keywords
        for key, keyword in self.KEYWORDS.items():
            self.listing_data[key] = self._get_element_next_to_string(keyword)

        # Extract description
        description_element = self.soup.find(attrs=self.DESCRIPTION_SELECTOR)
        self.listing_data["description"] = description_element.text if description_element else ""

        #logger.info(f"Extracted listing_data: {json.dumps(self.listing_data, indent=4)}") #TODO


    def get_listing_dict(self) -> Dict[str, Optional[str]]:
        """
        Returns the listing details as a dictionary.

        :return: A dictionary containing the listing details.
        """
        return self.listing_data