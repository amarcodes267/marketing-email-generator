# Architecture

## Overview

Personalized Marketing Copy AI is a full-stack web application with a Flask
backend that serves both the frontend UI and the AI-powered email generation API
from a single origin (single-URL app).

## Components

### Frontend (`frontend/`)

- `index.html` — Single-page UI with the customer form and generated-email output.
- `css/style.css` — Responsive, mobile-first stylesheet.
- `js/config.js` — Deployment configuration (backend API URL override).
- `js/script.js` — Form validation, API calls, notifications, copy/clear actions.

The frontend is served by Flask:

- `GET /` renders `index.html` (Flask `template_folder` → `frontend/`).
- `/css/...` and `/js/...` are served from `frontend/` (Flask `static_folder` → `frontend/`, `static_url_path=""`).

### Backend (`backend/`)

| Module                        | Responsibility                                                    |
|-------------------------------|-------------------------------------------------------------------|
| `app.py`                      | Flask app factory, CORS, blueprint registration, index route      |
| `config.py`                   | Environment-driven configuration                                  |
| `routes/email_routes.py`      | `/health` and `/generate-email` API endpoints                     |
| `services/email_service.py`   | Orchestrates enrichment + AI generation                           |
| `services/personalization_service.py` | Customer segmentation, loyalty, discount, tone, CTA       |
| `services/recommendation_service.py`  | Product recommendation by category/segment                 |
| `services/ai_service.py`      | Prompt building, Gemini API invocation, output parsing/cleaning   |
| `models/llm.py`               | Legacy local model stub (Gemini API is used for generation)       |
| `prompts/email_prompt.py`     | Builds the system/user prompt for the LLM                         |
| `utils/validator.py`          | Request validation                                               |
| `data/`                       | Data directory (reserved)                                         |

### Data flow

```
Browser (frontend/)
  │  POST /generate-email  (JSON)
  ▼
Flask route (backend/routes/email_routes.py)
  │  validate_email_request()
  ▼
services/email_service.generate_email()
  │  analyze_customer()  -> segmentation, discount, tone, CTA
  │  recommend_product() -> product recommendation
  ▼
services/ai_service.generate_ai_email()
  │  build_email_prompt()
  │  services/ai_service._generate_with_gemini()  (Gemini API inference)
  │  parse + clean AI output
  ▼
JSON response  { success, subject, email }
```

## Tech Stack

| Layer    | Technology                                    |
|----------|-----------------------------------------------|
| Frontend | HTML5, CSS3, Vanilla JavaScript (ES6+)        |
| Backend  | Python 3.12, Flask 3.1                        |
| AI / ML  | Gemini API via google-generativeai         |
| Infra    | Flask-CORS, Gunicorn, python-dotenv, pytest   |
| Testing  | pytest (32 unit + integration tests)          |

