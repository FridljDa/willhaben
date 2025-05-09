from src.get_listings import fetch_all_listings

# Example usage
if __name__ == "__main__":
    url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=30"
    listings = fetch_all_listings(url)
    print(listings)
