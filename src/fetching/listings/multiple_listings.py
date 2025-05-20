import json
import os
from pathlib import Path

import pandas as pd

from fetching.listings.single_listing import SingleListing


class MultipleListings:
  def __init__(self, path: str = None) -> None:
    self.path_json = Path(__file__).resolve().parent.parent / 'out' / 'listings.txt'
    self.path_csv = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'out',
                                 'listings.csv')
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
    """h
    Pretty prints the listing details in JSON format.
    """
    for listing in self.list_of_listings:
      listing.pretty_print()

  def list_of_listings_to_dict(self) -> list:
    """
    Returns the listing details as a list of dictionaries.
    """
    return [single_listing.listing_data for single_listing in self.list_of_listings]

  def read_and_return_multiple_listings_from_txt_json_file(self) -> list[SingleListing]:
    """
    Reads the listing details from a text file in JSON format.
    """
    with open(self.path_json, 'r', encoding='utf-8') as f:
      list_of_listings_json = json.load(f)
      return [SingleListing() for listing in list_of_listings_json]

  def write_multiple_listings_to_txt_json_file(self) -> None:
    """
    Writes the listing details to a text file in JSON format.
    """
    # convert list_of_listings to a list of dictionaries
    list_of_dictionary_listing = self.list_of_listings_to_dict()

    if not os.path.exists(self.path_json):
      os.makedirs(os.path.dirname(self.path_json), exist_ok=True)
      with open(self.path_json, 'w', encoding='utf-8') as f:
        pass

    with open(self.path_json, 'w', encoding='utf-8') as f:
      json.dump(list_of_dictionary_listing, f, indent=4, ensure_ascii=False)

  def read_and_return_multiple_listings_from_csv_file(self) -> list[SingleListing]:
    """
    Reads the listing details from a text file in JSON format.
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
    for listing in self.list_of_listings:
      listing.listing_data =  {key: listing.listing_data.get(key, None) for key in keys}


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