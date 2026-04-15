import os
from sambanova import SambaNova

client = SambaNova(
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

def generate_recipe_data(text: str):
    prompt = f"""
Extract recipe information from the text below.

IMPORTANT:
- Do NOT leave fields empty
- If exact values are missing, make reasonable guesses
- Focus on ingredients and instructions

Return ONLY valid JSON (no explanation)

FORMAT:

{{
  "title": "recipe name",
  "cuisine": "type",
  "prep_time": "value",
  "cook_time": "value",
  "total_time": "value",
  "servings": 2,
  "difficulty": "easy",
  "ingredients": [
    {{ "quantity": "2", "unit": "slices", "item": "bread" }}
  ],
  "instructions": [
    "step 1",
    "step 2"
  ],
  "nutrition": {{
    "calories": "approx",
    "protein": "approx",
    "carbs": "approx",
    "fat": "approx"
  }},
  "substitutions": [
    "suggestion 1",
    "suggestion 2"
  ],
  "shopping_list": {{
    "general": ["items"]
  }}
}}

TEXT:
{text[:4000]}
"""

    response = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content
