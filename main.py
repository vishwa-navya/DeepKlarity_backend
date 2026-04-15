from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import json

from database import SessionLocal, engine
from models import Base, Recipe
from scraper import scrape_recipe
from llm_service import generate_recipe_data

Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/extract")
def extract_recipe(url: str, db: Session = Depends(get_db)):
    raw_text = scrape_recipe(url)

    ai_response = generate_recipe_data(raw_text)

    try:
        data = json.loads(ai_response)
    except:
        return {"error": "Invalid AI response"}

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


@app.get("/recipes")
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).all()
