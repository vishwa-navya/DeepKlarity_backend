import os
from sambanova import SambaNova

client = SambaNova(
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

def generate_recipe_data(text: str):
    prompt = f"""
You are a strict JSON generator.

Extract recipe data from the given text and return ONLY valid JSON.

Do NOT include any explanation or text.

Return format:

{{
  "title": "",
  "cuisine": "",
  "prep_time": "",
  "cook_time": "",
  "total_time": "",
  "servings": 0,
  "difficulty": "",
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
  "shopping_list": {{}}
}}

TEXT:
{text}
"""

    response = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    return response.choices[0].message.content
