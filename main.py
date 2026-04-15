from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json
import re

from database import SessionLocal, engine
from models import Base, Recipe
from scraper import scrape_recipe
from llm_service import generate_recipe_data

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🔥 CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for assignment)
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

        # 🔥 Fallback if scraping fails
        if not raw_text or len(raw_text) < 200:
            raw_text = f"Extract recipe from this URL: {url}"

        # 🔹 Step 2: AI Processing
        ai_response = generate_recipe_data(raw_text)

        # 🔹 Step 3: Extract JSON safely
        try:
            json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)
            if not json_match:
                return {
                    "error": "No JSON found in AI response",
                    "raw_output": ai_response
                }

            json_str = json_match.group()
            data = json.loads(json_str)

        except Exception as e:
            return {
                "error": "AI did not return valid JSON",
                "details": str(e),
                "raw_output": ai_response
            }

        # 🔹 Step 4: Save to DB
        recipe = Recipe(
            url=url,
            title=data.get("title"),
            cuisine=data.get("cuisine", ""),
            difficulty=data.get("difficulty", ""),
            ingredients=data.get("ingredients", []),
            instructions=data.get("instructions", []),
            nutrition=data.get("nutrition", {}),
            substitutions=data.get("substitutions", []),
            shopping_list=data.get("shopping_list", {}),
        )

        db.add(recipe)
        db.commit()
        db.refresh(recipe)

        # 🔹 Step 5: Return response
        return data

    except Exception as e:
        return {
            "error": "Something went wrong in backend",
            "details": str(e)
        }


@app.get("/recipes")
def get_recipes(db: Session = Depends(get_db)):
    try:
        return db.query(Recipe).all()
    except Exception as e:
        return {
            "error": "Failed to fetch recipes",
            "details": str(e)
        }
