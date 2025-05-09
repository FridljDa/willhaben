import requests
from bs4 import BeautifulSoup

class SingleListing:
    """
    A class to represent a single listing.
    """

    soup = BeautifulSoup()

    url = str()
    wh_code = str()
    description = str()
    availability_start = str()
    availability_duration = str()
    number_rooms = str()
    size2 = str()

    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup()

    def get_soup(self):
        """
        Fetches the HTML content of a URL and returns a BeautifulSoup object.

        :param url: The URL to fetch.
        :return: A BeautifulSoup object of the page content.
        """
        url = self.url
        print('Getting listings from ' + url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def get_element_next_to_string(self, string_find):
        """
        Extracts the availability start date from the soup.

        :param soup: BeautifulSoup object of the page content.
        :param string_find: The string to search for in the soup.
        :return: The availability start date as a string, or None if not found.
        """
        soup = self.soup
        element = soup.find(string=string_find)
        if element is None:
            return None
        return element.find_next().text

    def fetch_set_single_listing_content(self):
        """
        Gets the listings from a URL.

        :param url: The URL to fetch listings from.
        :return: A dictionaries containing the listing.
        """

        product_page = requests.get(self.url)
        soup_pd = BeautifulSoup(product_page.content, 'html.parser')

        for heading in soup_pd.find_all("title"):
            heading_item = heading.text.strip("- willhaben")

        wh_code = str()
        for char in self.url[::-1]:
            if char.isnumeric():
                wh_code += char
            elif char == "-":
                break
        self.wh_code = wh_code[::-1]

        self.description = (soup_pd
                       .find(attrs={"data-testid": "ad-description-Objektbeschreibung"})
                       .text)

        self.availability_start = self.get_element_next_to_string("Verfügbar")
        self.availability_duration = self.get_element_next_to_string("Befristung")
        self.number_rooms = self.get_element_next_to_string("Zimmer")
        self.size2 = self.get_element_next_to_string("Wohnfläche")

    def get_listing_dict(self):
        """
        Gets the listings from a URL.

        :param url: The URL to fetch listings from.
        :return: A dictionaries containing the listing.
        """
        self.fetch_set_single_listing_content()

        listing = {
            "availability_start": self.availability_start,
            "availability_duration": self.availability_duration,
            "description": self.description,
            "number_rooms": self.number_rooms,
            "size2": self.size2,
            "wh_code": self.wh_code,
            "url": self.url
        }

        return listing

url_test = "https://www.willhaben.at/iad/immobilien/d/mietwohnungen/wien/wien-1030-landstrasse/provisionsfreie-moeblierte-wohnung-mit-perfekter-oeffentlicher-anbindung-in-1030-2007459668"
res = (SingleListing(url_test).get_listing_dict())
print(res)