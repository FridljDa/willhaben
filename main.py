from listing.fetcher.listing_details_fetcher import ListingDetailsFetcher
from listing.fetcher.listings_overview_fetcher import ListingsOverviewFetcher
from listing.structure.multiple_listings import MultipleListings
from relevant_columns import relevant_keys

if __name__ == "__main__":
    multiple_listings = MultipleListings()

    url_query = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=1000&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40'
    ListingsOverviewFetcher(url_query, multiple_listings).fetch_all_listings()
    multiple_listings.apply_function_to_each_listing(
        ListingDetailsFetcher.fetch_and_set_single_listing_content
    )

    multiple_listings.subselect_listing_keys_and(relevant_keys)

    multiple_listings.write_multiple_listings_to_txt_json_file()
    multiple_listings.write_multiple_listings_to_csv_file()

    multiple_listings.pretty_print()
    print(f"Number of listings: {len(multiple_listings.list_of_listings)}")
