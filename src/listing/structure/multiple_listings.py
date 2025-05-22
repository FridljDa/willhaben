import json
import os

import pandas as pd

from listing.structure.single_listing import SingleListing
from project_root import PROJECT_ROOT


class MultipleListings:
  def __init__(self, path: str = None) -> None:
    self.path_json = PROJECT_ROOT / 'out' / 'listings.txt'
    self.path_csv = PROJECT_ROOT / 'out' / 'listings.csv'

    if path is None:
      self.list_of_listings: list[SingleListing] = []
    elif path.endswith('.txt'):
      if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
      self.path_json = path
      self.list_of_listings = self.read_and_return_multiple_listings_from_txt_json_file()
    elif path.endswith('.csv'):
      if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
      self.path_csv = path
      self.list_of_listings = self.read_and_return_multiple_listings_from_csv_file()
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

  def read_and_return_multiple_listings_from_txt_json_file(self) -> list[
    SingleListing]:
    """
    Reads the listing details from a JSON file and returns a list of SingleListing objects.
    """
    with open(self.path_json, 'r', encoding='utf-8') as f:
      list_of_listings_json = json.load(f)
      return [SingleListing() for _ in list_of_listings_json]

  def write_multiple_listings_to_txt_json_file(self) -> None:
    """
    Writes the listing details to a JSON file.
    """
    list_of_dictionary_listing = self.list_of_listings_to_dict()

    os.makedirs(os.path.dirname(self.path_json), exist_ok=True)
    with open(self.path_json, 'w', encoding='utf-8') as f:
      json.dump(list_of_dictionary_listing, f, indent=4, ensure_ascii=False)

  def read_and_return_multiple_listings_from_csv_file(self) -> list[
    SingleListing]:
    """
    Reads the listing details from a CSV file and returns a list of SingleListing objects.
    """
    df = pd.read_csv(self.path_csv, encoding='utf-8')
    return [SingleListing() for _, row in df.iterrows()]

  def write_multiple_listings_to_csv_file(self) -> None:
    """
    Writes the listing details to a CSV file.
    """

    list_of_dictionary_listing = self.list_of_listings_to_dict()
    df = pd.DataFrame(list_of_dictionary_listing)
    df.to_csv(self.path_csv, index=False, encoding='utf-8')

  def subselect_listing_keys_and(self, keys: list) -> None:
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
