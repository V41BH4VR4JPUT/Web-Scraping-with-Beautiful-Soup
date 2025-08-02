import argparse
import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys

# Handle known exceptions in Wikipedia naming
def get_wiki_page_name(language):
    special_cases = {
        "C++": "C%2B%2B",
        "C#": "C_Sharp_(programming_language)",
        "F#": "F_Sharp_(programming_language)",
        "Go": "Go_(programming_language)",
        "R": "R_(programming_language)",
        "Rust": "Rust_(programming_language)",
        "Swift": "Swift_(programming_language)",
        "Python": "Python_(programming_language)",
        "Java": "Java_(programming_language)",
        "JavaScript": "JavaScript",
        "TypeScript": "TypeScript"
    }
    return special_cases.get(language, language.replace(" ", "_") + "_(programming_language)")

# Extract first paragraph from content
def extract_first_paragraph(soup):
    content_div = soup.find("div", {"id": "mw-content-text"})
    if content_div:
        paragraphs = content_div.find_all("p", recursive=True)
        for p in paragraphs:
            if p.text.strip():
                return p.text.strip()
    return "No paragraph found."

# Extract external links from "External links" section
def extract_external_links(soup):
    external_links = []
    for header in soup.find_all(["h2", "h3"]):
        if header.text.strip().lower().startswith("external links"):
            ul = header.find_next_sibling("ul")
            if ul:
                for li in ul.find_all("li"):
                    a_tag = li.find("a", href=True)
                    if a_tag and a_tag['href'].startswith("http"):
                        external_links.append((a_tag.text.strip(), a_tag['href']))
            break
    return external_links

# Extract all subheadings
def extract_subheadings(soup):
    content_div = soup.find("div", {"id": "mw-content-text"})
    headings = []
    for tag in content_div.find_all(["h2", "h3", "h4"]):
        text = tag.get_text(strip=True).replace("[edit]", "")
        if text:
            headings.append(text)
    return headings

# Extract "See also" internal links
def extract_see_also_links(soup):
    see_also_links = []
    for header in soup.find_all(["h2", "h3"]):
        if header.text.strip().lower().startswith("see also"):
            ul = header.find_next_sibling("ul")
            if ul:
                for li in ul.find_all("li"):
                    a_tag = li.find("a", href=True)
                    if a_tag and a_tag['href'].startswith("/wiki/"):
                        full_url = urllib.parse.urljoin("https://en.wikipedia.org", a_tag['href'])
                        see_also_links.append((a_tag.text.strip(), full_url))
            break
    return see_also_links

# Scrape and display main content
def scrape_wikipedia_page(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f" Failed to fetch page. HTTP Status: {response.status_code}")
            sys.exit(1)
        soup = BeautifulSoup(response.content, 'html.parser')
        h1_tag = soup.find("h1")
        title = h1_tag.text.strip() if h1_tag else "No title found"
        print(f"\n Title: {title}")

        print("\n First Paragraph:")
        print(extract_first_paragraph(soup))

        print("\n External Links:")
        links = extract_external_links(soup)
        if links:
            for text, link in links:
                print(f" - {text}: {link}")
        else:
            print(" - No external links found.")

        print("\n Subheadings:")
        headings = extract_subheadings(soup)
        for h in headings:
            print(f" - {h}")

        print("\n See Also:")
        see_also = extract_see_also_links(soup)
        if see_also:
            for idx, (text, link) in enumerate(see_also, start=1):
                print(f" [{idx}] {text}: {link}")
            try:
                choice = int(input("\nEnter the number of a 'See also' link to explore it (0 to skip): "))
                if 1 <= choice <= len(see_also):
                    selected_text, selected_url = see_also[choice - 1]
                    print(f"\nNavigating to: {selected_text} ({selected_url})")
                    scrape_wikipedia_page(selected_url)
                else:
                    print("Skipped navigation.")
            except ValueError:
                print("Invalid input. Skipped navigation.")
        else:
            print(" - No 'See also' section found.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

# Main entry
def main():
    parser = argparse.ArgumentParser(description="Wikipedia Article Navigator for Programming Languages")
    parser.add_argument("-p", "--programming-language", required=True, help="Name of the programming language")
    args = parser.parse_args()
    language = args.programming_language

    page_name = get_wiki_page_name(language)
    wiki_url = f"https://en.wikipedia.org/wiki/{page_name}"
    print(f"Fetching Wikipedia page for: {language}\nURL: {wiki_url}")
    scrape_wikipedia_page(wiki_url)

if __name__ == "__main__":
    main()
