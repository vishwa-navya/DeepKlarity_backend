import requests
from bs4 import BeautifulSoup

def scrape_recipe(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()
