# approach 1

import requests
from bs4 import BeautifulSoup

def get_availability_start(soup, string_find):
    """
    Extracts the availability start date from the soup.

    :param soup: BeautifulSoup object of the page content.
    :param string_find: The string to search for in the soup.
    :return: The availability start date as a string, or None if not found.
    """
    element = soup.find(string=string_find)
    if element is None:
        return None
    return element.find_next().text

def get_single_listing(url):
    """
    Gets the listings from a URL.

    :param url: The URL to fetch listings from.
    :return: A dictionaries containing the listing.
    """

    print('Getting listings from ' + url)

    product_page = requests.get(url)
    soup_pd = BeautifulSoup(product_page.content, 'html.parser')

    for heading in soup_pd.find_all("title"):
        heading_item = heading.text.strip("- willhaben")

    wh_code = str()
    for char in url[::-1]:
        if char.isnumeric():
            wh_code += char
        elif char == "-":
            break
    wh_code = wh_code[::-1]

    description = (soup_pd
                   .find(attrs={"data-testid": "ad-description-Objektbeschreibung"})
                   .text)

    availability_start = get_availability_start(soup_pd, "Verfügbar")

    availability_duration = get_availability_start(soup_pd, "Befristung")

    listing = {
        "availability_start": availability_start,
        "availability_duration": availability_duration,
        "description": description,
        "wh_code": wh_code,
        "url": url
    }

    return listing

url_test = "https://www.willhaben.at/iad/immobilien/d/mietwohnungen/wien/wien-1030-landstrasse/provisionsfreie-moeblierte-wohnung-mit-perfekter-oeffentlicher-anbindung-in-1030-2007459668"
res = get_single_listing(url_test)
print(res)