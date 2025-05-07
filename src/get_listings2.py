# approach 1

import requests
import os

from bs4 import BeautifulSoup
from colorama import Fore


def get_listings2(url):
    """
    Gets the listings from a URL.

    :param url: The URL to fetch listings from.
    :return: A dictionaries containing the listing.
    """

    name_adding = 0
    product_page = requests.get(url)
    soup_pd = BeautifulSoup(product_page.content, 'html.parser')

    soup_pd.find(string="ab 01.06.2025")

    for heading in soup_pd.find_all("title"):
        heading_item = heading.text.strip("- willhaben")

    wh_code = str()
    for char in url[::-1]:
        if char.isnumeric():
            wh_code += char
        elif char == "-":
            break
    wh_code = wh_code[::-1]

    description = soup_pd.find(attrs={"data-testid": "ad-description-Objektbeschreibung"}).text

    availability_start = (soup_pd.find(string="Verfügbar")
                          .find_next()
                          .text)

    availability_duration = (soup_pd.find(string="Befristung")
                             .find_next()
                             .text)


    if not os.path.exists("Results/" + wh_code):
        os.makedirs("Results/" + wh_code)


    infos = open("Results/" + wh_code + f"/Infos {wh_code}.txt", "w", encoding='utf-8',
                 errors='replace')
    infos.write("Titel, Price, ZIP and Place:\n")
    infos.write(heading_item)
    infos.write("\n----------------------------------------------\n")
    infos.write("Description:\n")
    infos.write(description)
    infos.write("\n----------------------------------------------\n")
    #infos.write("attributevalue:\n")
    #infos.write(attributevalue)
    infos.write("\n----------------------------------------------\n")
    infos.write("Willhaben Link:\n")
    infos.write(url)
    infos.write("\n----------------------------------------------\n")
    infos.close()

    print(Fore.GREEN + f"-----------------------\nGrabbing completed.\n-----------------------" + Fore.CYAN)

url_test = "https://www.willhaben.at/iad/immobilien/d/mietwohnungen/wien/wien-1030-landstrasse/provisionsfreie-moeblierte-wohnung-mit-perfekter-oeffentlicher-anbindung-in-1030-2007459668"
get_listings2(url_test)