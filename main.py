from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import json

from database import SessionLocal, engine
from models import Base, Recipe
from scraper import scrape_recipe
from llm_service import generate_recipe_data

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# ✅ DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ EXTRACT API (FINAL VERSION)
@app.post("/extract")
def extract_recipe(url: str, db: Session = Depends(get_db)):
    try:
        # 🔥 Step 1: Scrape content
        raw_text = scrape_recipe(url)

        if not raw_text or len(raw_text) < 100:
            return {
                "error": "Failed to scrape content or content too small"
            }

        # 🔥 Step 2: Send to AI
        ai_response = generate_recipe_data(raw_text)

        # 🔥 Step 3: Convert AI response → JSON
        try:
            data = json.loads(ai_response)
        except Exception as e:
            return {
                "error": "AI did not return valid JSON",
                "details": str(e),
                "raw_output": ai_response[:500]
            }

        # 🔥 Step 4: Save to DB
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

        # ✅ Step 5: Return clean response
        return data

    except Exception as e:
        return {
            "error": "Something went wrong in backend",
            "details": str(e)
        }


# ✅ GET HISTORY (LATEST FIRST)
@app.get("/recipes")
def get_recipes(db: Session = Depends(get_db)):
    try:
        recipes = db.query(Recipe).order_by(Recipe.id.desc()).all()
        return recipes
    except Exception as e:
        return {
            "error": "Failed to fetch recipes",
            "details": str(e)
        }
