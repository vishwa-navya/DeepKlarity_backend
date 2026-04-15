import requests
from bs4 import BeautifulSoup
import json

def scrape_recipe(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        # If blocked or empty
        if response.status_code != 200 or not response.text:
            return "Failed to fetch page"

        soup = BeautifulSoup(response.text, "html.parser")

        # 🔥 Extract ALL JSON-LD scripts
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            try:
                data = json.loads(script.string)

                # Case 1: List of objects
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("@type") == "Recipe":
                            return json.dumps(item)

                # Case 2: Direct object
                if isinstance(data, dict) and data.get("@type") == "Recipe":
                    return json.dumps(data)

            except Exception:
                continue

        # 🔁 FALLBACK (VERY IMPORTANT)
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text(strip=True) for p in paragraphs])

        # Ensure something is returned
        if len(text) > 100:
            return text

        return "No usable content found"

    except Exception as e:
        return f"Error: {str(e)}"
