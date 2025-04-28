import requests
import json

def get_listings(url):
    """
    Gets the listings from a URL.

    :param url: The URL to fetch listings from.
    :return: A list of dictionaries containing the listings.
    """
    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
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
        listings = []
        advert_summaries = parsed_data['props']['pageProps']['searchResult']['advertSummaryList']['advertSummary']
        for advert in advert_summaries:
            # Flatten the attributes into the main dictionary
            for attribute in advert['attributes']['attribute']:
                name = attribute['name'].lower()
                value = attribute['values'][0]
                advert[name] = int(value) if value.isdigit() else value

            # Remove unnecessary keys
            keys_to_remove = ['attributes', 'contextLinkList', 'advertiserInfo', 'advertImageList']
            for key in keys_to_remove:
                advert.pop(key, None)

            listings.append(advert)

        return listings

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
if __name__ == "__main__":
    url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=30"
    listings = get_listings(url)
    print(listings)