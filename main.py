from app import get_listings

# Example usage
if __name__ == "__main__":
    url = "https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=30"
    listings = get_listings(url)
    print(listings)
