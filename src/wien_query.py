import json

from src.get_listings import fetch_all_listings
from get_single_listing import SingleListing

url_query = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=30&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40'

listings = fetch_all_listings(url_query)

for listing in listings:
    listing['full_url'] = 'https://www.willhaben.at/iad/' + listing['seo_url']
    more_keys = (SingleListing(listing['full_url']).get_listing_dict())
    listing.update(more_keys)

# Filter the listings to include only the selected keys
selected_keys = ['location', 'postcode', 'description', 'heading', 'body_dyn', 'price', 'size', 'seo_url']
selected_keys = ['heading', 'price', 'size', 'full_url', 'availability_start', 'availability_duration']
listings = [
    {key: listing.get(key, None) for key in selected_keys}
    for listing in listings
]

print(json.dumps(listings, indent=4, ensure_ascii=False))
print(f"Number of listings: {len(listings)}")

# Save listings to a JSON file
with open('../out/listings.txt', 'w', encoding='utf-8') as f:
    json.dump(listings, f, indent=4, ensure_ascii=False)

#keywords = ['sublet', 'months', 'october', 'december', 'monate', 'kurzzeit']
# Filter listings for those containing any of the keywords in heading, body_dyn, or description
#filtered_listings = [
#    listing for listing in listings
#    if any(keyword in (listing.get('heading', '') + listing.get('body_dyn', '') + listing.get('description', '')).lower()
#           for keyword in keywords)
#]

#filtered_listings = [
#    listing for listing in listings
#    if decide_if_is_sublet(listing)
#]

# Uncomment the following line to print the filtered listings
#print(filtered_listings)