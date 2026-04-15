import os
from sambanova import SambaNova

client = SambaNova(
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

def generate_recipe_data(text: str):
    prompt = f"""
You are a smart recipe extractor.

The input is full HTML of a recipe webpage.

Extract:
- title
- ingredients
- instructions

IMPORTANT:
- Do NOT leave empty
- Infer if needed
- Ignore HTML tags

Return ONLY JSON:

{{
  "title": "",
  "ingredients": [
    {{ "quantity": "", "unit": "", "item": "" }}
  ],
  "instructions": []
}}

HTML:
{text[:6000]}
"""

    response = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content
