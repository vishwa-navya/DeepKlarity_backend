import requests
from bs4 import BeautifulSoup

def scrape_recipe(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Bad status:", response.status_code)
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        # 🔥 Extract meaningful content only
        texts = []

        for tag in soup.find_all(["p", "li", "h1", "h2"]):
            text = tag.get_text(strip=True)
            if text:
                texts.append(text)

        combined = " ".join(texts)

        # 🔥 Relaxed filter
        if len(combined) < 100:
            print("Too small content")
            return ""

        return combined

    except Exception as e:
        print("Scraping error:", e)
        return ""
