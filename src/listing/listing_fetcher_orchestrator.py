from pathlib import Path

from listing.fetcher.listing_details_fetcher import ListingDetailsFetcher
from listing.fetcher.listings_overview_fetcher import ListingsOverviewFetcher
from listing.structure.multiple_listings import ListingRepository
from relevant_columns import relevant_keys


class ListingFetcherOrchestrator:
  def __init__(self, url_query, path: Path = None, silent=True):
    self.url_query = url_query
    self.multiple_listings = ListingRepository(path=path)
    self.silent = silent

  def fetch_and_process_listings(self):
    ListingsOverviewFetcher(self.url_query,
                            self.multiple_listings).fetch_all_listings()

    self.multiple_listings.apply_function_to_each_listing(
        lambda single_listing: ListingDetailsFetcher(
            single_listing).fetch_and_set_single_listing_content()
    )

    self.multiple_listings.select_listing_keys_and(relevant_keys)

    if not self.silent:
      self.multiple_listings.pretty_print()
      print(
        f"Number of listings: {len(self.multiple_listings.list_of_listings)}")

  def write_listings_to_files(self):
    self.multiple_listings.write_multiple_listings_to_txt_json_file()
    self.multiple_listings.write_multiple_listings_to_csv_file()
