# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "requests>=2.31.0",
#     "beautifulsoup4>=4.12.2",
# ]
# ///

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


def scrape_links_by_pattern(url, pattern):
    """
    Fetches a webpage and scrapes links matching a specific pattern (like
    magnet links or .torrent files).

    NOTE: Always ensure you have permission to scrape a website 
    and adhere to its terms of service and robots.txt file.

    Args:
        url (str): The URL of the webpage to scrape.
        pattern (str): The regex pattern to match against the link 'href'
                       attributes (e.g., r'^magnet:').
    Returns:
        list: A list of unique links that match the pattern.
    """
    print(f"--- Attempting to fetch: {url} ---")

    # 1. Fetch the webpage content
    try:
        # Use a common user-agent header to avoid being blocked
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    # 2. Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # 3. Compile the regex pattern
    link_pattern = re.compile(pattern)

    # 4. Find all <a> tags and check their 'href' attributes
    found_links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]

        # Check if the href matches the target pattern
        if link_pattern.search(href):
            # If it's a relative URL (e.g., /download/file.torrent), make it absolute
            absolute_link = urljoin(url, str(href))
            found_links.add(absolute_link)

    return list(found_links)


if __name__ == "__main__":
    # --- Configuration ---
    # Replace this with the URL of the page you want to scrape.
    # We use a placeholder URL here for safe execution.
    target_url = "http://example.com/some_page"

    # --- Example Patterns ---

    # Pattern 1: Find Magnet Links (Starts with 'magnet:')
    magnet_pattern = r"^magnet:"
    magnet_links = scrape_links_by_pattern(target_url, magnet_pattern)

    print("\n--- Found Magnet Links ---")
    if magnet_links:
        for link in magnet_links:
            print(link)
    else:
        print("No magnet links found matching the pattern.")

    # Pattern 2: Find .torrent file downloads (Ends with '.torrent')
    torrent_file_pattern = r"\.torrent$"
    torrent_links = scrape_links_by_pattern(target_url, torrent_file_pattern)

    print("\n--- Found .torrent File Links ---")
    if torrent_links:
        for link in torrent_links:
            print(link)
    else:
        print("No .torrent file links found matching the pattern.")

    # NOTE: Since the target_url is 'example.com', which contains no such links,
    # the output will likely show zero links found.
