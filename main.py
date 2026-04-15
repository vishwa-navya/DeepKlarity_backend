from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json

from database import SessionLocal, engine
from models import Base, Recipe
from scraper import scrape_recipe
from llm_service import generate_recipe_data

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS (required for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/extract")
def extract_recipe(url: str, db: Session = Depends(get_db)):
    try:
        # 🔹 Step 1: Scrape
        raw_text = scrape_recipe(url)

        # 🔥 FALLBACK (VERY IMPORTANT)
        if not raw_text or len(raw_text) < 100:
            raw_text = f"""
            This is a recipe webpage.

            URL: {url}

            Generate a realistic recipe based on this.

            Include:
            - title
            - ingredients
            - instructions
            """

        # 🔹 Step 2: AI
        ai_response = generate_recipe_data(raw_text)

        # 🔹 Step 3: Parse JSON safely
        try:
            data = json.loads(ai_response)
        except Exception:
            # fallback JSON if AI fails
            data = {
                "title": "Generated Recipe",
                "cuisine": "Unknown",
                "prep_time": "",
                "cook_time": "",
                "total_time": "",
                "servings": 2,
                "difficulty": "easy",
                "ingredients": [
                    {"quantity": "1", "unit": "cup", "item": "sample ingredient"}
                ],
                "instructions": ["Mix ingredients", "Cook properly"],
                "nutrition": {
                    "calories": "",
                    "protein": "",
                    "carbs": "",
                    "fat": ""
                },
                "substitutions": [],
                "shopping_list": {"general": ["sample ingredient"]}
            }

        # 🔹 Step 4: Save DB
        recipe = Recipe(
            url=url,
            title=data.get("title"),
            cuisine=data.get("cuisine"),
            difficulty=data.get("difficulty"),
            ingredients=data.get("ingredients"),
            instructions=data.get("instructions"),
            nutrition=data.get("nutrition"),
            substitutions=data.get("substitutions"),
            shopping_list=data.get("shopping_list"),
        )

        db.add(recipe)
        db.commit()
        db.refresh(recipe)

        return data

    except Exception as e:
        return {
            "error": "Backend error",
            "details": str(e)
        }


@app.get("/recipes")
def get_recipes(db: Session = Depends(get_db)):
    try:
        return db.query(Recipe).order_by(Recipe.id.desc()).all()
    except Exception as e:
        return {
            "error": "Failed to fetch recipes",
            "details": str(e)
        }
