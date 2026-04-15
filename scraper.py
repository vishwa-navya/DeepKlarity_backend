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

    # 🔥 BEST METHOD: Extract JSON-LD (structured data)
    script = soup.find("script", type="application/ld+json")

    if script:
        try:
            data = json.loads(script.string)

            # Handle list format
            if isinstance(data, list):
                data = data[0]

            # Extract useful fields
            title = data.get("name", "")
            ingredients = data.get("recipeIngredient", [])
            instructions_data = data.get("recipeInstructions", [])

            instructions = []
            for step in instructions_data:
                if isinstance(step, dict):
                    instructions.append(step.get("text", ""))
                else:
                    instructions.append(str(step))

            content = f"Title: {title}. Ingredients: {ingredients}. Instructions: {instructions}"

            return content

        except Exception:
            pass

    # 🔁 FALLBACK (if JSON-LD not found)
    paragraphs = soup.find_all("p")
    text = " ".join([p.get_text(strip=True) for p in paragraphs])

    return text
