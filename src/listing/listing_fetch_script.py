from listing.fetcher.listing_details_fetcher import ListingDetailsFetcher
from listing.fetcher.listings_overview_fetcher import ListingsOverviewFetcher
from listing.structure.multiple_listings import MultipleListings
from relevant_columns import relevant_keys


def fetch_and_process_listings(url_query):
  multiple_listings = MultipleListings()

  ListingsOverviewFetcher(url_query, multiple_listings).fetch_all_listings()

  multiple_listings.apply_function_to_each_listing(
      lambda single_listing: ListingDetailsFetcher(
        single_listing).fetch_and_set_single_listing_content()
  )

  multiple_listings.subselect_listing_keys_and(relevant_keys)

  multiple_listings.write_multiple_listings_to_txt_json_file()
  multiple_listings.write_multiple_listings_to_csv_file()

  multiple_listings.pretty_print()
  print(f"Number of listings: {len(multiple_listings.list_of_listings)}")


if __name__ == "__main__":
  fetch_and_process_listings()
