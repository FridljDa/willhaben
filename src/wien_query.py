from src.get_listings import get_listings
from src.prompt_parser import decide_if_is_sublet

url_query = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=30&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40'

listings = get_listings(url_query)

# Filter the listings to include only the selected keys
selected_keys = ['location', 'postcode', 'description', 'heading', 'body_dyn', 'price', 'size', 'seo_url']
listings = [
    {key: listing.get(key, None) for key in selected_keys}
    for listing in listings
]

keywords = ['sublet', 'months', 'october', 'december', 'monate', 'kurzzeit']

# Filter listings for those containing any of the keywords in heading, body_dyn, or description
#filtered_listings = [
#    listing for listing in listings
#    if any(keyword in (listing.get('heading', '') + listing.get('body_dyn', '') + listing.get('description', '')).lower()
#           for keyword in keywords)
#]

filtered_listings = [
    listing for listing in listings
    if decide_if_is_sublet(listing)
]

# Uncomment the following line to print the filtered listings
print(filtered_listings)