from listing_details_fetcher import ListingDetailsFetcher
from src.listings_overview_fetcher import ListingsOverviewFetcher
from src.multiple_listings import MultipleListings

if __name__ == "__main__":
    multiple_listings = MultipleListings()

    url_query = 'https://www.willhaben.at/iad/immobilien/mietwohnungen/mietwohnung-angebote?sort=1&rows=100&isNavigation=true&sfId=7c07d0eb-68b5-46e8-8e40-e47a743a85b0&ESTATE_PREFERENCE=28&areaId=117223&areaId=117224&areaId=117225&areaId=117226&areaId=117227&areaId=117228&areaId=117229&areaId=117230&areaId=117231&page=1&PRICE_FROM=0&PRICE_TO=1100&ESTATE_SIZE/LIVING_AREA_FROM=40'
    ListingsOverviewFetcher(url_query, multiple_listings).fetch_all_listings()
    multiple_listings.apply_function_to_each_listing(
        ListingDetailsFetcher.fetch_and_set_single_listing_content
    )

    relevant_keys = [
        'ADDITIONAL_COST/DEPOSIT',
        'ADDITIONAL_COST/FEE',
        'AVAILABLE_DATE',
        'BUILDING_CONDITION',
        'BUILDING_TYPE',
        'Befristung',
        'DESCRIPTION',
        'DURATION/HASTERMLIMIT',
        'DURATION/TERMLIMITTEXT',
        'ESTATE_PREFERENCE',
        'ESTATE_SIZE',
        'ESTATE_SIZE/LIVING_AREA',
        'FLOOR',
        'FLOOR_SURFACE',
        'GENERAL_TEXT_ADVERT/Lage',
        'GENERAL_TEXT_ADVERT/Sonstiges',
        'HEATING',
        'ISPRIVATE',
        'LOCATION/ADDRESS_1',
        'LOCATION/ADDRESS_2',
        'LOCATION/ADDRESS_3',
        'LOCATION/ADDRESS_4',
        'NO_OF_ROOMS',
        'OWNAGETYPE',
        'PRICE',
        'PRICE_FOR_DISPLAY',
        'PROPERTY_TYPE',
        'PROPERTY_TYPE_FLAT',
        'RENTAL_PRICE/ADDITIONAL_COST_GROSS',
        'RENTAL_PRICE/HEATINGCOSTSGROSS',
        'RENTAL_PRICE/PER_MONTH',
        'RENTAL_PRICE/PER_MONTH_FOR_DISPLAY',
        'RENTAL_PRICE/TOTAL_ENCUMBRANCE',
        'Verfuegbarkeit',
        'available_date',
        'url'
    ]
    multiple_listings.subselect_listing_keys_and(relevant_keys)

    multiple_listings.write_multiple_listings_to_txt_json_file()
    multiple_listings.write_multiple_listings_to_csv_file()

    multiple_listings.pretty_print()
    print(f"Number of listings: {len(multiple_listings.list_of_listings)}")
