# Personalized Marketing Copy AI

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-orange)](https://flask.palletsprojects.com/)
[![Render Ready](https://img.shields.io/badge/Render-Ready-brightgreen)](https://render.com/)

## Overview
Personalized Marketing Copy AI is a full-stack web application that generates tailored marketing email copy from customer profile data. The backend builds a structured prompt from the submitted form details and uses the Gemini API to generate an email subject line and body.

This solution is ideal for teams, marketers, and developers who want a simple, deployable example of AI-assisted email generation without running a heavy local model.

## What It Does
- Converts customer profile data into a polished marketing email
- Segments audiences based on customer type, spend, and preferences
- Recommends product suggestions and discount strategies
- Supports selectable email tones such as Friendly, Luxury, Urgent, and Promotional
- Uses Gemini API for cloud-based generation via `GOOGLE_API_KEY`
- Cleans and parses generated output into structured subject and body fields
- Provides Render-compatible deployment configuration out of the box

## Why This Project
Marketing campaigns perform better when messaging is personalized. This app demonstrates how to take customer data and quickly produce campaign-ready email copy using AI.

It is useful for:
- marketing teams generating campaign drafts
- startups validating AI content workflows
- developers exploring prompt engineering and API integration

## Technology Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- AI: Gemini API via `google-generativeai`
- Deployment: Render

## Repository Structure
- `backend/` — Flask app, API endpoints, services, prompts, configuration
- `frontend/` — static UI files served by the backend
- `docs/` — architecture, API, and deployment documentation
- `render.yaml` — Render deployment blueprint
- `.env.example` — template for environment configuration

## Prerequisites
Before running the project, ensure you have:
- Python 3.11 or newer
- `pip` installed
- a valid Google API key with Gemini access
- Git (recommended for cloning the repository)

## Local Setup
Follow these steps to run the application locally.

### 1. Clone the repository
```bash
git clone https://github.com/amarcodes267/marketing-email-generator.git
cd marketing-email-generator
```

### 2. Prepare environment variables
Copy the sample environment file:
```bash
copy .env.example .env
```
Then update `.env` with your Gemini API key:
```dotenv
FLASK_ENV=development
FLASK_DEBUG=true
HOST=0.0.0.0
PORT=5000

MODEL_NAME=gemini-1.5
GENAI_MODEL_NAME=gemini-1.5
MAX_NEW_TOKENS=250
GENERATION_TIMEOUT_SECONDS=300
MAX_REQUEST_BODY_BYTES=65536
GOOGLE_API_KEY=<your_google_api_key>
```

### 3. Install dependencies
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

Open your browser at `http://localhost:5000`.

## Configuration
The backend uses `backend/config.py` to load environment variables.

### Important configuration values
- `FLASK_ENV` — `development` or `production`
- `FLASK_DEBUG` — enable debug mode locally
- `HOST` — host address for Flask
- `PORT` — application port
- `MODEL_NAME` — Gemini model name
- `GENAI_MODEL_NAME` — optional Gemini model alias
- `MAX_NEW_TOKENS` — maximum output tokens
- `GENERATION_TIMEOUT_SECONDS` — API request timeout
- `MAX_REQUEST_BODY_BYTES` — limit for request payload size
- `GOOGLE_API_KEY` — Gemini API key

## API Reference
The application exposes a single endpoint for email generation.

### POST `/generate-email`
This endpoint accepts JSON payloads describing customer data and email preferences.

#### Request payload example
```json
{
  "customer_name": "Alex",
  "age": 28,
  "gender": "Female",
  "location": "Austin, TX",
  "favorite_category": "Home",
  "total_spent": 420,
  "purchase_history": "kitchen appliances, home decor",
  "tone": "Friendly",
  "discount_percentage": 15
}
```

#### Response example
```json
{
  "success": true,
  "subject": "Alex, your home refresh is ready with a special offer",
  "email": "Hi Alex, ..."
}
```

## Application Flow
1. User submits customer profile data through the frontend.
2. Flask validates and enriches the request.
3. `backend/services/ai_service.py` builds a prompt and invokes Gemini.
4. Gemini returns generated content.
5. The backend cleans and parses the AI output.
6. The formatted subject and email body are returned to the frontend.

## AI Generation Process
The AI generation path is implemented in `backend/services/ai_service.py`:
- load the `GOOGLE_API_KEY` from the environment
- configure Gemini client
- create a prompt from the request data
- call `genai_client.generate()`
- validate response and extract the text
- clean the result and split it into subject and body

### Prompt generation
The prompt template is defined in `backend/prompts/email_prompt.py`. It uses customer data, product recommendations, and tone settings to construct a contextual input for Gemini.

## Output Cleanup
The project includes several cleaning and parsing routines to produce usable email content:
- remove placeholders and system artifacts
- normalize punctuation and whitespace
- remove irrelevant trailing sections
- ensure the output contains both subject and body

## Deployment
This repository is ready for Render deployment.

### Render setup
Use `render.yaml` to define the Render service blueprint.

#### Render service configuration
- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 600 --workers 1`
- Health check path: `/health`

#### Render environment variables
Set these values in Render:
- `FLASK_ENV=production`
- `HOST=0.0.0.0`
- `MODEL_NAME=gemini-1.5`
- `GENAI_MODEL_NAME=gemini-1.5`
- `MAX_NEW_TOKENS=250`
- `GENERATION_TIMEOUT_SECONDS=300`
- `MAX_REQUEST_BODY_BYTES=65536`
- `GOOGLE_API_KEY=<your_google_api_key>`

> Render auto-injects `PORT`, so do not set it manually.

### Recommended Render settings
- Plan: `free` or `starter`
- Region: `oregon`
- Build hooks: disabled unless required
- Auto deploy from GitHub: enabled

## Troubleshooting
### Common issues
**`GOOGLE_API_KEY is not set`**
- Ensure `GOOGLE_API_KEY` exists in `.env` or in Render environment variables.

**Timeouts or partial responses**
- Increase `GENERATION_TIMEOUT_SECONDS`.
- Lower `MAX_NEW_TOKENS` if the model response is too long.
- Confirm the Gemini API key is valid and not rate-limited.

**Frontend not loading**
- Make sure Flask is running and listening on the correct port.
- Verify the browser is loading `http://localhost:5000`.

**Deployment failures**
- Check Render logs for build or runtime errors.
- Confirm the correct root directory and start command are configured.

## Security
- Keep `GOOGLE_API_KEY` private.
- Do not commit `.env` or API keys to source control.
- Use environment variables for secrets in production.

## Development Notes
- `backend/models/llm.py` is retained as a legacy stub; the production path uses Gemini.
- `backend/services/email_service.py` orchestrates data enrichment and AI generation.
- `backend/services/personalization_service.py` handles segmentation and tone.
- `backend/services/recommendation_service.py` provides product recommendations.
- `backend/utils/validator.py` validates request payloads.

## Future Improvements
Potential next steps include:
- adding user authentication
- adding rate limiting
- supporting multiple Gemini models
- providing a campaign management dashboard
- exporting generated email content to CSV or PDF

## Contribution
Contributions are welcome. To contribute:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with a clear summary

## License
This project is licensed under the MIT License.

## Contact
For questions or support, open an issue in the repository or email the maintainer.
