"""
Web Crawler Module
Fetches web pages and extracts links for crawling.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Set, List, Dict
import time


class WebCrawler:
    """Simple web crawler that fetches pages and follows links."""

    def __init__(self, max_pages: int = 50, delay: float = 0.5):
        """
        Initialize the crawler.

        Args:
            max_pages: Maximum number of pages to crawl
            delay: Delay between requests in seconds (be polite!)
        """
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls: Set[str] = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Educational-SearchEngine-Bot/1.0'
        })

    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and should be crawled."""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme) and parsed.scheme in ['http', 'https']
        except:
            return False

    def fetch_page(self, url: str) -> Dict:
        """
        Fetch a single page and extract its content.

        Returns:
            Dict with 'url', 'title', 'content', and 'links'
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()

            # Extract title
            title = soup.find('title')
            title = title.get_text().strip() if title else url

            # Extract text content
            text = soup.get_text(separator=' ', strip=True)

            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                if self.is_valid_url(absolute_url):
                    links.append(absolute_url)

            return {
                'url': url,
                'title': title,
                'content': text,
                'links': links
            }

        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def crawl(self, seed_urls: List[str], same_domain: bool = True) -> List[Dict]:
        """
        Crawl web pages starting from seed URLs.

        Args:
            seed_urls: List of starting URLs
            same_domain: If True, only crawl pages on the same domain

        Returns:
            List of crawled pages
        """
        to_visit = seed_urls.copy()
        crawled_pages = []
        seed_domain = urlparse(seed_urls[0]).netloc if same_domain and seed_urls else None

        while to_visit and len(self.visited_urls) < self.max_pages:
            url = to_visit.pop(0)

            # Skip if already visited
            if url in self.visited_urls:
                continue

            # Check domain restriction
            if same_domain and seed_domain:
                if urlparse(url).netloc != seed_domain:
                    continue

            print(f"Crawling ({len(self.visited_urls) + 1}/{self.max_pages}): {url}")

            page_data = self.fetch_page(url)

            if page_data:
                self.visited_urls.add(url)
                crawled_pages.append(page_data)

                # Add new links to queue
                for link in page_data['links']:
                    if link not in self.visited_urls and link not in to_visit:
                        to_visit.append(link)

                # Be polite - delay between requests
                time.sleep(self.delay)

        print(f"\nCrawling complete! Fetched {len(crawled_pages)} pages.")
        return crawled_pages


if __name__ == "__main__":
    # Example usage
    crawler = WebCrawler(max_pages=10)

    # Crawl a small site for testing
    seed_urls = [
        "https://en.wikipedia.org/wiki/Search_engine"
    ]

    pages = crawler.crawl(seed_urls, same_domain=True)

    for page in pages[:3]:
        print(f"\nTitle: {page['title']}")
        print(f"URL: {page['url']}")
        print(f"Content preview: {page['content'][:200]}...")
