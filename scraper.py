import requests
from bs4 import BeautifulSoup
import json

def scrape_recipe(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # 🔥 Extract ALL JSON-LD scripts
    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        try:
            data = json.loads(script.string)

            # Some pages have list of objects
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") == "Recipe":
                        return json.dumps(item)

            # Direct object
            if isinstance(data, dict) and data.get("@type") == "Recipe":
                return json.dumps(data)

        except:
            continue

    # ❌ fallback (if nothing found)
    return ""
