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
You are a professional chef AI.

Generate or extract a complete recipe.

IMPORTANT RULES:
- NEVER return empty fields
- ALWAYS generate a valid recipe
- Even if input is unclear, create a realistic recipe
- Return ONLY valid JSON

FORMAT:
{{
  "title": "",
  "cuisine": "",
  "prep_time": "",
  "cook_time": "",
  "total_time": "",
  "servings": 2,
  "difficulty": "easy",
  "ingredients": [
    {{ "quantity": "", "unit": "", "item": "" }}
  ],
  "instructions": [],
  "nutrition": {{
    "calories": "",
    "protein": "",
    "carbs": "",
    "fat": ""
  }},
  "substitutions": [],
  "shopping_list": {{
    "general": []
  }}
}}

INPUT:
{text[:1500]}
"""

    for _ in range(2):  # retry for rate limit
        try:
            response = client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )

            content = response.choices[0].message.content.strip()

            # 🔥 Clean markdown if exists
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()

            return content

        except Exception as e:
            if "rate limit" in str(e).lower():
                time.sleep(2)
            else:
                break

    # 🔥 FINAL GUARANTEE (never fail)
    return json.dumps({
        "title": "Homemade Recipe",
        "cuisine": "Generic",
        "prep_time": "10 mins",
        "cook_time": "15 mins",
        "total_time": "25 mins",
        "servings": 2,
        "difficulty": "easy",
        "ingredients": [
            {"quantity": "1", "unit": "cup", "item": "flour"},
            {"quantity": "1", "unit": "cup", "item": "milk"}
        ],
        "instructions": [
            "Mix all ingredients",
            "Cook properly",
            "Serve hot"
        ],
        "nutrition": {
            "calories": "200",
            "protein": "5g",
            "carbs": "30g",
            "fat": "5g"
        },
        "substitutions": [],
        "shopping_list": {
            "general": ["flour", "milk"]
        }
    })
