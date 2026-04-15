
import requests
from bs4 import BeautifulSoup

def scrape_recipe(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
        list_items = [li.get_text(strip=True) for li in soup.find_all("li")]
        content = " ".join(headings + paragraphs + list_items)

        
        content = " ".join(content.split())

        return content

    except Exception as e:
        return f"Error scraping: {str(e)}"
