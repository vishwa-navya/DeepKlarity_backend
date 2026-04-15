import os
import time
import json
from sambanova import SambaNova

client = SambaNova(
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

def generate_recipe_data(text: str):
    prompt = f"""
You are a strict JSON generator.

Extract recipe data from the given text and return ONLY valid JSON.

Return this exact format:

{{
  "title": "",
  "cuisine": "",
  "prep_time": "",
  "cook_time": "",
  "total_time": "",
  "servings": 0,
  "difficulty": "",
  "ingredients": [],
  "instructions": [],
  "nutrition": {{
    "calories": "",
    "protein": "",
    "carbs": "",
    "fat": ""
  }},
  "substitutions": [],
  "shopping_list": {{}}
}}

TEXT:
{text[:4000]}
"""

    for attempt in range(2):  # retry 2 times
        try:
            response = client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
            )

            content = response.choices[0].message.content.strip()

            # 🔥 CLEAN JSON (important)
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()

            return content

        except Exception as e:
            print("AI Error:", str(e))

            if "rate limit" in str(e).lower():
                time.sleep(2)  # wait and retry
            else:
                break

    # ❌ FINAL FALLBACK (NO CRASH)
    return json.dumps({
        "title": "Unknown Recipe",
        "cuisine": "Unknown",
        "prep_time": "",
        "cook_time": "",
        "total_time": "",
        "servings": 0,
        "difficulty": "unknown",
        "ingredients": [],
        "instructions": [],
        "nutrition": {
            "calories": "",
            "protein": "",
            "carbs": "",
            "fat": ""
        },
        "substitutions": [],
        "shopping_list": {}
    })
