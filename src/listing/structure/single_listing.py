import logging
import pprint
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SingleListing:
  """
    A class to represent a single listing.
  """

  def __init__(self) -> None:
    self.listing_data = {}

  def pretty_print(self) -> None:
    """h
    Pretty prints the listing details in JSON format.
    """
    pprint.pprint(self.listing_data)

  def get_listing_dict(self) -> Dict[str, Optional[str]]:
    """
    Returns the listing details as a dictionary.

    :return: A dictionary containing the listing details.
    """
    return self.listing_data

  def add_key_value_pair(self, key: str, value: str) -> None:
    """
    Adds a key-value pair to the listing data.

    :param key: The key to add.
    :param value: The value to add.
    """
    self.update_dict({key: value})

  def update_dict(self, new_listing_data: dict[str, str]) -> None:
    """
    Updates the listing data with the provided dictionary.

    :param new_listing_data: The dictionary to update.
    """
    for key, value in new_listing_data.items():
      if key and value:
        self.listing_data[key] = value
      else:
        logger.debug(f"Key or value is None. Key: {key}, Value: {value}")
