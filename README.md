# Personalized Marketing Copy AI

Generate AI-powered personalized marketing emails using customer demographics, purchase history, and behavioral analytics — powered by an open-source Hugging Face language model running locally.

## Project Overview

Personalized Marketing Copy AI is a full-stack web app that turns raw customer information into compelling, personalized marketing emails. It:

- Collects customer demographics (name, age, gender, location) and purchase behavior (history, favorite category, total spending).
- Analyzes the customer to determine segment, spending level, loyalty status, and optimal discount.
- Recommends the most relevant product based on the customer's favorite category.
- Builds a context-rich prompt combining insights, tone, and call-to-action.
- Uses **TinyLlama-1.1B-Chat** (Hugging Face) to generate a unique email with a matching subject line.
- Cleans, parses, and validates the AI output to deliver a polished final email.

No API keys. No paid services. Fully open source and CPU-compatible.

## Features

- AI-generated personalized marketing emails via TinyLlama (Hugging Face).
- Customer segmentation (New / Regular / Premium / VIP).
- Spending level, loyalty status detection, and dynamic discounts (5%-20%).
- Product recommendation engine by category and segment.
- 16 configurable email tones (Friendly, Luxury, Urgent, Promotional, and more).
- Intelligent prompt builder with structured customer analytics.
- Robust AI output parser with subject extraction and content cleaning.
- Full-stack validation, loading spinner, toasts, copy-to-clipboard, clear-form.
- Responsive, accessible, mobile-first UI.
- Thread-safe model loaded once at startup; CPU inference, no GPU required.

## Tech Stack

| Layer    | Technology                                    |
|----------|-----------------------------------------------|
| Frontend | HTML5, CSS3, Vanilla JavaScript (ES6+)        |
| Backend  | Python 3.12, Flask 3.1                        |
| AI / ML  | Hugging Face Transformers, PyTorch, TinyLlama |
| Infra    | Flask-CORS, Gunicorn, python-dotenv, pytest   |
| Testing  | pytest (32 unit + integration tests)          |

## Installation

Prerequisites: Python 3.12+, pip, and internet (first-time model download; cached afterward).

```bash
git clone https://github.com/YOUR_USERNAME/genai-marketing-copy.git
cd genai-marketing-copy
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
cd backend
pip install -r requirements.txt
```

> First run downloads the TinyLlama model (~2.3 GB), then it is cached locally.

## How to Run

**Backend:** `cd backend && python app.py` - server runs on `http://0.0.0.0:5000`. Health check: `GET http://localhost:5000/`.

**Frontend:** Navigate to `frontend/` and open `index.html` directly (calls the local Flask API at `http://localhost:5000`), or serve with `python -m http.server 8000` and visit `http://localhost:8000`.

## API Endpoints

### `GET /`

Health check. Returns `200` with `{"message": "Marketing Copy AI Backend Running"}`.

### `POST /generate-email`

Generates a personalized marketing email.

**Request body (all required):**

| Field               | Constraints                                            |
|---------------------|--------------------------------------------------------|
| `customer_name`     | Max 80 characters                                      |
| `age`               | 18 - 100                                               |
| `gender`            | `Male`, `Female`, `Other`                              |
| `location`          | Max 120 characters                                     |
| `purchase_history`  | Max 2000 characters (newline-separated)                |
| `favorite_category` | `Fashion`, `Electronics`, `Books`, `Sports`, `Home Decor`, `Beauty` |
| `total_spending`    | Greater than 0                                         |
| `tone`              | One of the 16 supported tones                          |

**Example request:** `{"customer_name": "Priya", "age": 32, "gender": "Female", "location": "Bangalore", "purchase_history": "Designer Dress\nHeels", "favorite_category": "Fashion", "total_spending": 70000, "tone": "Luxury"}`

**Example response `200`:** `{"success": true, "subject": "An Exclusive Luxury Collection Awaits You, Priya", "email": "Dear Priya,\n\nAt ShopEasy, we believe you deserve nothing less than the extraordinary..."}`

**Errors:** `400` invalid fields · `413` body too large · `415` wrong Content-Type · `500` AI/server error.

## Deployment on Render

This project includes a `render.yaml` (Render Blueprint) that deploys **two services**: a Flask backend API and a static frontend site.

### Files for deployment

| File | Purpose |
|------|---------|
| `render.yaml` | Render Blueprint — defines the backend (Python) and frontend (Static) services |
| `backend/runtime.txt` | Pins Python 3.12.10 for the backend |
| `frontend/js/config.js` | Lets the frontend point to the deployed backend URL |

### Steps on Render

1. **Push this repository to GitHub** (already done for `amarcodes267/marketing-email-generator`).

2. **Connect the repo on Render**:
   - Go to [render.com](https://render.com) → **New +** → **Blueprint** → select your GitHub repo.
   - Render reads `render.yaml` and creates both services automatically:
     - `marketing-copy-backend` (Flask API, free web service)
     - `marketing-copy-frontend` (static site, free static service)

3. **Deploy the backend first** — wait until it says **Live**. The first deploy downloads the TinyLlama model (~2.3 GB) and may take several minutes.

4. **Copy your backend URL** — e.g. `https://marketing-copy-backend.onrender.com`.

5. **Point the frontend at the backend**:
   - Edit `frontend/js/config.js` and set:
     ```js
     window.MARKETING_AI_API_URL = 'https://marketing-copy-backend.onrender.com';
     ```
   - Commit and push — Render auto-redeploys the frontend.

6. **Done** — open your frontend URL (`https://marketing-copy-frontend.onrender.com`) and test.

### Important notes

- **Free tier memory:** Render free web services have **512 MB RAM**. TinyLlama (~2.3 GB) may exceed this. If generation fails with memory errors, either upgrade the backend instance (paid tier) or set `MODEL_NAME` to a smaller model.
- **Cold starts:** Free services spin down after inactivity; the first request after idle may take time while the model reloads.
- **Health check:** Render uses `GET /` on the backend, which returns the health check response.

## Testing

```bash
cd backend
pytest tests/ -v
```

Expected: **32 tests passed**.

## Troubleshooting

| Issue                                  | Solution                                             |
|----------------------------------------|------------------------------------------------------|
| `ModuleNotFoundError` on startup       | Run `pip install -r requirements.txt` in your venv   |
| Slow model download on first run       | TinyLlama is ~2.3 GB; use a stable connection        |
| Port 5000 already in use               | Set `PORT` to a different value (e.g., `5001`)       |
| Browser shows "Unable to reach server" | Ensure Flask backend is running on `localhost:5000`  |
| Generation request times out           | Increase `GENERATION_TIMEOUT_SECONDS`                |
| `gunicorn` fails on Windows            | Gunicorn is Linux-only; use `python app.py` locally  |
| Out-of-memory during model load        | Ensure at least 4 GB free RAM for TinyLlama          |
