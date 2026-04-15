import os
from sambanova import SambaNova

client = SambaNova(
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

def generate_recipe_data(text: str):
    prompt = f"""
You are an intelligent recipe extraction system.

From the given webpage text, extract structured recipe data.

IMPORTANT RULES:
- Return ONLY valid JSON
- Do NOT include any explanation or extra text
- If some fields are missing, intelligently infer values
- Fill as much data as possible

JSON FORMAT:

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

    try:
        response = client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.9,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error from AI: {str(e)}"
