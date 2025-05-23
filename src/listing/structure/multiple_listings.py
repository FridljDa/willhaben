from pathlib import Path

import pandas as pd

from listing.structure.single_listing import SingleListing
from project_root import PROJECT_ROOT
from relevant_columns import dtypes_columns


class MultipleListings:
  def __init__(self, path: Path = None) -> None:
    self.path_csv = PROJECT_ROOT / 'out' / 'listings.csv'

    if path is None:
      self.list_of_listings: list[SingleListing] = []
    elif path.suffix == '.csv':
      if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
      self.path_csv = path
    else:
      raise ValueError(
          "Unsupported file type. Only .txt or .csv files are allowed.")

  def pretty_print(self) -> None:
    """
    Pretty prints the listing details in JSON format.
    """
    for listing in self.list_of_listings:
      listing.pretty_print()

  def list_of_listings_to_dict(self) -> list:
    """
    Returns the listing details as a list of dictionaries.
    """
    return [single_listing.listing_data for single_listing in
            self.list_of_listings]

  def read_and_set_multiple_listings_from_csv_file(self) -> None:
    """
    Reads the listing details from a CSV file and returns a list of SingleListing objects.
    """
    df = pd.read_csv(
        self.path_csv,
        encoding='utf-8',
        dtype=dtypes_columns
    )
    # TODO parse dates
    self.list_of_listings = [SingleListing() for _, row in df.iterrows()]

  def multiple_listings_to_pandas_dataframe(self) -> pd.DataFrame:
    """
    Converts the list of listings to a pandas DataFrame.
    """
    list_of_dictionary_listing = self.list_of_listings_to_dict()

    df = pd.DataFrame(
        list_of_dictionary_listing)

    # TODO use .astype(dtypes_columns))
    return df

  def write_multiple_listings_to_csv_file(self) -> None:
    """
    Writes the listing details to a CSV file.
    """
    df = self.multiple_listings_to_pandas_dataframe()
    df.to_csv(self.path_csv, index=False, encoding='utf-8')

  def select_listing_keys_and(self, keys: list) -> None:
    """
    Filters the listing data to only include specified keys.

    Args:
        keys (list): A list of keys to retain in each listing's data.
    """
    if not keys:
      raise ValueError("The keys list cannot be empty.")
    for listing in self.list_of_listings:
      listing.listing_data = {key: listing.listing_data.get(key, None) for key
                              in keys}

  def apply_function_to_each_listing(self, function) -> None:
    """
    Applies a function to each listing in the list_of_listings.
    """
    for listing in self.list_of_listings:
      function(listing)

  def append_listing(self, listing: SingleListing) -> None:
    """
    Appends a listing to the list_of_listings.
    """
    self.list_of_listings.append(listing)
