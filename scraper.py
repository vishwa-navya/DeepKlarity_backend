import requests

def scrape_recipe(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # 🔥 Send FULL HTML (not cleaned text)
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"
