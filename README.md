# DeepKlarity Backend

## 🚀 Overview
This is the backend service for the DeepKlarity Recipe Extraction Application.  
It extracts recipe information from a given URL using web scraping and AI processing.

---

## 🛠 Tech Stack
- Python
- FastAPI
- PostgreSQL (Render)
- SQLAlchemy
- BeautifulSoup (Web Scraping)
- SambaNova AI (LLM)

---

## ⚙️ Architecture

1. User sends recipe URL from frontend
2. Backend attempts to scrape content using BeautifulSoup
3. If scraping fails (due to bot blocking), fallback logic is used
4. AI model processes the content and generates structured JSON
5. Data is stored in PostgreSQL
6. Response is sent back to frontend

---

## 🔥 Key Features

- AI-powered recipe extraction
- Smart fallback when scraping fails
- Structured JSON response
- Database storage for history
- Error handling for:
  - Rate limits
  - Invalid AI responses
  - Scraping failures

---

## 🌐 API Endpoints

### POST /extract
Extract recipe from URL

Query param:

url: string


---

### GET /recipes
Fetch all extracted recipes (latest first)

---

## 🧠 Design Decisions

- Scraping is unreliable due to anti-bot protection, so AI fallback is implemented
- JSON validation ensures frontend stability
- Retry + fallback prevents system crashes

---

## ⚠️ Known Limitations

- Some websites block scraping (handled using AI fallback)
- Free AI APIs have rate limits

---

## 🚀 Deployment

- Hosted on Render
- Uses PostgreSQL database (Render)

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
🔑 Environment Variables
SAMBANOVA_API_KEY=your_api_key
DATABASE_URL=your_postgres_url
