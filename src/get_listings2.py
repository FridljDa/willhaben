# approach 1
import requests
import json

# approach 2
import requests
from bs4 import BeautifulSoup

#should be inspired by https://github.com/ramyodev/Willhaben-Grabber/tree/main/src

def get_listings(url):
    """
    Gets the listings from a URL.

    :param url: The URL to fetch listings from.
    :return: A list of dictionaries containing the listings.
    """

    product_page = requests.get(url)
    soup_pd = BeautifulSoup(product_page.content, 'html.parser')

    listings = []

    return listings


url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=30"
listings = get_listings(url)
print(listings)