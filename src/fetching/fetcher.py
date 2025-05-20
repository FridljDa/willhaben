import json
import logging
from typing import re

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NEXT_DATA_START = '<script id="__NEXT_DATA__" type="application/json">'
NEXT_DATA_END = '</script>'

class Fetcher:
  def __init__(self, url: str):
    # Replace &rows=<some number>& in the URL with &rows=1000&
    self.url = re.sub(r"&rows=\d+&", "&rows=1000&", url)

  @staticmethod
  def fetch_json_from_url(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text
    return Fetcher.extract_json_data(html_content)

  @staticmethod
  def extract_json_data(html_content: str) -> dict:
    """
    Extracts JSON data from the HTML content.

    :param html_content: The HTML content as a string.
    :return: The extracted JSON data as a string.
    """
    try:
      start_index = html_content.find(NEXT_DATA_START) + len(NEXT_DATA_START)
      end_index = html_content.find(NEXT_DATA_END, start_index)
      html_content = html_content[start_index:end_index]
      return json.loads(html_content)
    except ValueError:
      logger.error("Failed to locate JSON data in the HTML content.")
      return {}