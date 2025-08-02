import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys

def extract_articles(url, num_articles=5):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f" Failed to fetch page. HTTP Status: {response.status_code}")
            sys.exit(1)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Inspecting DEV.to shows articles in <h2> inside <a> tags with class "crayons-story__title"
        article_elements = soup.find_all("a", class_="crayons-story__hidden-navigation-link", limit=num_articles)

        if not article_elements:
            print(" No articles found. The page structure might have changed.")
            return

        print(f"\n Top {len(article_elements)} Articles from {url}:\n")
        for idx, article in enumerate(article_elements, start=1):
            title = article.text.strip()
            href = article["href"] if hasattr(article, "get") and article.has_attr("href") else None # type: ignore
            if isinstance(href, str):
                link = urljoin("https://dev.to", href)
            else:
                link = "N/A"
            print(f" {idx}. {title}\n    Link: {link}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Blog Article Extractor")
    parser.add_argument("-u", "--url", required=True, help="URL of the blog/category page to scrape")
    parser.add_argument("-n", "--num-articles", type=int, default=5, help="Number of articles to extract (default: 5)")
    args = parser.parse_args()

    extract_articles(args.url, args.num_articles)

if __name__ == "__main__":
    main()
