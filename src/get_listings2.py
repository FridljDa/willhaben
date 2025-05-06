# approach 1
import requests
import json

# approach 2
import requests
import os
import sys
import random
import time
import re

from bs4 import BeautifulSoup
from colorama import Fore


def get_listings2(url):
    name_adding = 0
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

    #<div data-testid="ad-description-Objektbeschreibung" class="Box-sc-wfmb7k-0 sc-e43c8c17-1 dOPEeS">
    description = soup_pd.find(attrs={"data-testid": "ad-description-Objektbeschreibung"}).text
    #soup_pd.text
    #heading.contents[0]
    #<div data-testid="attribute-value" class="Box-sc-wfmb7k-0 sc-a3477a6e-1 kHICiY">ab 01.06.2025</div>
    attributevalue = soup_pd.find(
        attrs={"data-testid": "attributevalue"})
    attributevalue = attributevalue.text

    #<div class="Box-sc-wfmb7k-0"><h2 class="Text-sc-10o2fdq-0 fAgrJT">Objektinformationen</h2><div data-testid="attribute-group" class="Box-sc-wfmb7k-0 fdqsae"><div class="Box-sc-wfmb7k-0 Columns-sc-1kewbr2-0 gnrgqv fgGYDD"><ul class="sc-a3477a6e-0 gqxkPB"><li data-testid="attribute-item" class="Box-sc-wfmb7k-0 sc-a3477a6e-2 gpGqgd guwAPD"><div data-testid="attribute-title" class="Box-sc-wfmb7k-0 jZqwIq"><span class="Text-sc-10o2fdq-0 hWtQkP">Objekttyp</span></div><div data-testid="attribute-value" class="Box-sc-wfmb7k-0 sc-a3477a6e-1 kHICiY">Wohnung</div></li><li data-testid="attribute-item" class="Box-sc-wfmb7k-0 sc-a3477a6e-2 gpGqgd guwAPD"><div data-testid="attribute-title" class="Box-sc-wfmb7k-0 jZqwIq"><span class="Text-sc-10o2fdq-0 hWtQkP">Bautyp</span></div><div data-testid="attribute-value" class="Box-sc-wfmb7k-0 sc-a3477a6e-1 kHICiY">Neubau</div></li><li data-testid="attribute-item" class="Box-sc-wfmb7k-0 sc-a3477a6e-2 gpGqgd guwAPD"><div data-testid="attribute-title" class="Box-sc-wfmb7k-0 jZqwIq"><span class="Text-sc-10o2fdq-0 hWtQkP">Zustand</span></div><div data-testid="attribute-value" class="Box-sc-wfmb7k-0 sc-a3477a6e-1 kHICiY">Renoviert</div></li><li data-testid="attribute-item" class="Box-sc-wfmb7k-0 sc-a3477a6e-2 gpGqgd guwAPD"><div data-testid="attribute-title" class="Box-sc-wfmb7k-0 jZqwIq"><span class="Text-sc-10o2fdq-0 hWtQkP">Wohnfläche</span></div><div data-testid="attribute-value" class="Box-sc-wfmb7k-0 sc-a3477a6e-1 kHICiY">49 m²</div></li><li data-testid="attribute-item" class="Box-sc-wfmb7k-0 sc-a3477a6e-2 gpGqgd guwAPD"><div data-testid="attribute-title" class="Box-sc-wfmb7k-0 jZqwIq"><span class="Text-sc-10o2fdq-0 hWtQkP">Zimmer</span></div><div data-testid="attribute-value" class="Box-sc-wfmb7k-0 sc-a3477a6e-1 kHICiY">1</div></li><li data-testid="attribute-item" class="Box-sc-wfmb7k-0 sc-a3477a6e-2 gpGqgd guwAPD"><div data-testid="attribute-title" class="Box-sc-wfmb7k-0 jZqwIq"><span class="Text-sc-10o2fdq-0 hWtQkP">Stockwerk(e)</span></div><div data-testid="attribute-value" class="Box-sc-wfmb7k-0 sc-a3477a6e-1 kHICiY">1</div></li><li data-testid="attribute-item" class="Box-sc-wfmb7k-0 sc-a3477a6e-2 gpGqgd guwAPD"><div data-testid="attribute-title" class="Box-sc-wfmb7k-0 jZqwIq"><span class="Text-sc-10o2fdq-0 hWtQkP">Verfügbar</span></div><div data-testid="attribute-value" class="Box-sc-wfmb7k-0 sc-a3477a6e-1 kHICiY">ab 01.06.2025</div></li><li data-testid="attribute-item" class="Box-sc-wfmb7k-0 sc-a3477a6e-2 gpGqgd guwAPD"><div data-testid="attribute-title" class="Box-sc-wfmb7k-0 jZqwIq"><span class="Text-sc-10o2fdq-0 hWtQkP">Befristung</span></div><div data-testid="attribute-value" class="Box-sc-wfmb7k-0 sc-a3477a6e-1 kHICiY">3 Jahre mit Verlängerungsoption</div></li><li data-testid="attribute-item" class="Box-sc-wfmb7k-0 sc-a3477a6e-2 gpGqgd guwAPD"><div data-testid="attribute-title" class="Box-sc-wfmb7k-0 jZqwIq"><span class="Text-sc-10o2fdq-0 hWtQkP">Heizung</span></div><div data-testid="attribute-value" class="Box-sc-wfmb7k-0 sc-a3477a6e-1 kHICiY">Gasheizung</div></li></ul></div></div></div>

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
    infos.write("attributevalue:\n")
    infos.write(attributevalue)
    infos.write("\n----------------------------------------------\n")
    infos.write("Willhaben Link:\n")
    infos.write(url)
    infos.write("\n----------------------------------------------\n")
    infos.close()

    print(Fore.GREEN + f"-----------------------\nGrabbing completed.\n-----------------------" + Fore.CYAN)

url_test = "https://www.willhaben.at/iad/immobilien/d/mietwohnungen/wien/wien-1030-landstrasse/provisionsfreie-moeblierte-wohnung-mit-perfekter-oeffentlicher-anbindung-in-1030-2007459668"
get_listings2(url_test)