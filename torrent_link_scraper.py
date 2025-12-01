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
import argparse
import os


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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.\
                36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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
            # If it's a relative URL (e.g., /download/file.torrent), 
            # make it absolute
            absolute_link = urljoin(url, str(href))
            found_links.add(absolute_link)

    return list(found_links)


def get_urls_from_args():
    """
    Parses command-line arguments to get the list of URLs to scrape.
    """
    parser = argparse.ArgumentParser(
        description="Web scraper for finding magnet or .torrent links.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Define a mutually exclusive group: you must provide EITHER a URL
    # OR a file, but not both.
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--url", type=str, help="The single URL of the webpage to scrape."
    )

    group.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to a file containing a list of URLs, one per line.",
    )

    args = parser.parse_args()

    urls = []

    if args.url:
        urls.append(args.url)
    elif args.file:
        file_path = args.file
        if not os.path.exists(file_path):
            print(f"Error: File not found at '{file_path}'")
            return []

        try:
            with open(file_path, "r") as f:
                # Read lines, strip whitespace, and filter out empty lines
                urls = [line.strip() for line in f if line.strip()]
        except IOError as e:
            print(f"Error reading file '{file_path}': {e}")
            return []

    return urls


if __name__ == "__main__":
    # Get the list of URLs from command line arguments
    target_urls = get_urls_from_args()

    if not target_urls:
        print("No valid URLs provided. Exiting.")
    else:
        # Define patterns once
        magnet_pattern = r"^magnet:"
        torrent_file_pattern = r"\.torrent$"

        # Loop through each URL provided (either one from --url or many from --file)
        for url in target_urls:
            print("\n========================================================")
            print(f"SCRAPING RESULTS FOR: {url}")
            print("========================================================")

            # Pattern 1: Find Magnet Links (Starts with 'magnet:')
            magnet_links = scrape_links_by_pattern(url, magnet_pattern)

            print("\n--- Found Magnet Links ---")
            if magnet_links:
                for link in magnet_links:
                    print(link)
            else:
                print(f"No magnet links found on {url}")

            # Pattern 2: Find .torrent file downloads (Ends with '.torrent')
            torrent_links = scrape_links_by_pattern(url, torrent_file_pattern)

            print("\n--- Found .torrent File Links ---")
            if torrent_links:
                for link in torrent_links:
                    print(link)
            else:
                print(f"No .torrent file links found on {url}")

        print("\n========================================================")
        print("SCRAPING COMPLETE.")
        print("========================================================")
