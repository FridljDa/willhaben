import json
import logging
import re
from pathlib import Path
from urllib.parse import urlparse

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NEXT_DATA_START = '<script id="__NEXT_DATA__" type="application/json">'
NEXT_DATA_END = '</script>'


class Fetcher:
  def __init__(self, url: str):
    parsed_url = urlparse(url)
    self.is_url = parsed_url.scheme in ("http", "https")

    if self.is_url:
      self.url = re.sub(r"&rows=\d+&", "&rows=1000&", url)
    else:
      self.url = url

  def fetch_content_as_json(self) -> dict:
    """
    Fetches the HTML content from a URL or local file path and extracts JSON data.

    :param url: The URL or file path to fetch content from.
    :return: The extracted JSON data as a dictionary.
    """
    if self.is_url:
      # It's a URL
      # Placeholder for json_handler.JsonHandler.fetch_content_as_json
      # response = json_handler.JsonHandler.fetch_content_as_json(source)
      response = requests.get(self.url)  # Fallback to requests for now
      response.raise_for_status()
      html_content = response.text
      return Fetcher.extract_json_from_html(html_content)
    else:
      # It's a local file path
      file_path = Path(self.url)
      html_content = file_path.read_text(encoding="utf-8")
      return json.loads(html_content)

  @staticmethod
  def extract_json_from_html(html_content: str) -> dict:
    """
    Extracts JSON data embedded in the HTML content.

    :param html_content: The HTML content as a string.
    :return: The extracted JSON data as a dictionary.
    """
    try:
      start_index = html_content.find(NEXT_DATA_START) + len(NEXT_DATA_START)
      end_index = html_content.find(NEXT_DATA_END, start_index)
      json_data = html_content[start_index:end_index]
      return json.loads(json_data)
    except ValueError:
      logger.error("Failed to locate JSON data in the HTML content.")
      return {}
