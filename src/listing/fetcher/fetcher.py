import json
import logging
from pathlib import Path
from typing import re
from urllib.parse import urlparse

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
    html_content = Fetcher.fetch_html2(url)
    return Fetcher.extract_json_data_dict(html_content)

  @staticmethod
  def fetch_html2(url_path: str) -> str:
    """
    Fetches the HTML content from a URL or local file path.

    :param url_path: The URL or file path to fetch content from.
    :return: The HTML content as a string.
    """
    parsed = urlparse(url_path)
    if parsed.scheme in ("http", "https"):
      # It's a URL
      # Placeholder for json_handler.JsonHandler.fetch_json_from_url
      # response = json_handler.JsonHandler.fetch_json_from_url(url_path)
      response = requests.get(url_path)  # Fallback to requests for now
      response.raise_for_status()
      return response.text
    else:
      # It's a local file path
      file_path = Path(url_path)
      return file_path.read_text(encoding="utf-8")

  @staticmethod
  def extract_json_data_dict(html_content: str) -> dict:
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

  @staticmethod
  def extract_json_data_str(html_content: str) -> str:
      """
      Extracts JSON data from the HTML content.

      :param html_content: The HTML content as a string.
      :return: The extracted JSON data as a string.
      """
      try:
        start_index = html_content.find(NEXT_DATA_START)
        if start_index == -1:
          raise ValueError("Start marker for JSON data not found.")
        start_index += len(NEXT_DATA_START)
        end_index = html_content.find(NEXT_DATA_END, start_index)
        if end_index == -1:
          raise ValueError("End marker for JSON data not found.")
        return html_content[start_index:end_index]
      except ValueError as e:
        logger.error(f"Failed to locate JSON data in the HTML content: {e}")
        return ""