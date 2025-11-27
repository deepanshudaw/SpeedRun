import requests
from bs4 import BeautifulSoup
from typing import List

BASE_URL = "https://en.wikipedia.org/wiki/"

# Wikipedia returns 403 if requests look like bots; use a simple browser UA.
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    ),
}

# ----------------------------------------------------------------------
# Fetch raw HTML for a Wikipedia page title
# ----------------------------------------------------------------------
def fetch_html(title: str) -> str:
    """
    Fetch the HTML content of a Wikipedia article by title.

    Args:
        title (str): Page title (e.g., 'Python_(programming_language)')

    Returns:
        str: Raw HTML of the page.
    """
    # Normalize to Wikipedia URL format
    url = BASE_URL + title.replace(" ", "_")

    # Supply a real User-Agent to avoid 403 responses from Wikipedia.
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.text


# ----------------------------------------------------------------------
# Extract Wikipedia hyperlinks from page HTML
# ----------------------------------------------------------------------
def extract_wiki_links(html: str) -> List[str]:
    """
    Extract outbound Wikipedia article links from a page's HTML.

    Args:
        html (str): Raw HTML content.

    Returns:
        list[str]: Unique Wikipedia article titles linked from the page.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Main article content block
    content = soup.find("div", {"id": "mw-content-text"})
    if content is None:
        return []

    links = set()

    for a in content.find_all("a", href=True):
        href = a["href"]

        # Only keep main namespace Wiki pages
        if not href.startswith("/wiki/"):
            continue

        # Exclude non-article namespaces
        if any(
            href.startswith(prefix)
            for prefix in [
                "/wiki/Special:",
                "/wiki/Talk:",
                "/wiki/Help:",
                "/wiki/Category:",
                "/wiki/Template:",
                "/wiki/File:",
                "/wiki/Portal:",
                "/wiki/Wikipedia:",
            ]
        ):
            continue

        title = href[len("/wiki/") :]

        # Clean anchors (e.g., "#History")
        title = title.split("#")[0]

        if title:
            links.add(title)

    return sorted(list(links))


# ----------------------------------------------------------------------
# Convenience function: directly get links from a title
# ----------------------------------------------------------------------
def get_links_from_title(title: str) -> List[str]:
    """
    Shortcut for: fetch_html(title) → extract_wiki_links(html)

    Args:
        title (str): Wikipedia page title.

    Returns:
        list[str]: Linked article titles.
    """
    html = fetch_html(title)
    return extract_wiki_links(html)


# ----------------------------------------------------------------------
# Manual test
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Quick test from CLI
    test_title = "India"
    print(f"Fetching links from: {test_title}")
    links = get_links_from_title(test_title)
    print(f"Found {len(links)} links.")
    for l in links[:20]:
        print(" -", l)
