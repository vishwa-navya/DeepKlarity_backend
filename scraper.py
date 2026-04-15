import requests

def scrape_recipe(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # Return HTML if available
        if response.status_code == 200 and response.text:
            return response.text

        return ""

    except:
        return ""
