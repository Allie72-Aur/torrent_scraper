# Torrent Link Scraper

A lightweight Python utility for scraping magnet links (`magnet:`) and direct
`.torrent` file download links from specified web pages. The script is designed for
flexibility, allowing users to process individual URLs or lists of URLs from a file.

## Disclaimer and Ethics

**This tool is intended for educational purposes only.** Users are responsible for
ensuring they comply with all legal requirements and website terms of service (TOS)
and respect the `robots.txt` file of any site they scrape. Do not use this tool for
unauthorized or illegal activities.

## Prerequisites

You need Python 3 installed on your system. The script relies on the following
third-party libraries:

- `requests`: To fetch the HTML content from the internet.
- `BeautifulSoup4` (`bs4`): To parse the HTML and navigate the document structure.

### Installation

Install the required Python packages using `pip`:

```bash
pip install requests beautifulsoup4
```

## Usage

The script requires you to specify **either** a URL or a file path.

### 1\. Scraping a Single URL

Use the `--url` flag followed by the full URL of the page you want to scrape.

```bash
python torrent_link_scraper.py --url "http://example.com/page-to-scrape"
```

### 2\. Batch Scraping from a File

Use the `-f` or `--file` flag followed by the path to a plain text file. The file must contain one complete URL per line.

**Example `urls.txt` content:**

```urls.txt
https://example.com/page1
https://testsite.net/page2
http://another-site.org/archive
```

**Execution:**

```bash
python torrent_link_scraper.py -f urls.txt
# OR
python torrent_link_scraper.py --file path/to/your/urls.txt
```

### 3\. Help Command

You can view the full help message and available options using:

```bash
python torrent_link_scraper.py --help
```

## License

This project is open-source. Please refer to the repository's license file
(if present) for details.
