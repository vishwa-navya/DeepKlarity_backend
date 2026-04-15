import requests
from bs4 import BeautifulSoup

def scrape_recipe(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    content = []

    # Extract title
    title = soup.find("h1")
    if title:
        content.append(title.get_text(strip=True))

    # Extract ingredients
    ingredients = soup.find_all("span", class_="ingredients-item-name")
    for ing in ingredients:
        content.append(ing.get_text(strip=True))

    # Extract instructions
    steps = soup.find_all("div", class_="paragraph")
    for step in steps:
        content.append(step.get_text(strip=True))

    return " ".join(content)
