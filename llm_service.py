import os
from sambanova import SambaNova

client = SambaNova(
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

def generate_recipe_data(text: str):
    prompt = f"""
You are a smart recipe extractor.

Extract recipe details from the input.

IMPORTANT:
- Do NOT return empty values
- If input is URL, still generate recipe
- Infer missing values if needed

Return ONLY valid JSON.

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
{text[:4000]}
"""

    try:
        response = client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error from AI: {str(e)}"
