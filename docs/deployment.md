# Deployment

## Local Development

### Prerequisites

- Python 3.12+
- pip
- Internet access (first run downloads the smaller model, then caches it)

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/genai-marketing-copy.git
cd genai-marketing-copy
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
cd backend
pip install -r requirements.txt
```

### Run

```bash
cd backend
python app.py
```

The server runs on `http://0.0.0.0:5000`.

- `GET http://localhost:5000/` — frontend UI
- `GET http://localhost:5000/health` — health check
- `POST http://localhost:5000/generate-email` — API

> **Note:** `gunicorn` is Linux-only. Use `python app.py` locally on Windows.

## Deployment on Render (single URL)

The project includes a `render.yaml` (Render Blueprint) that deploys one service.
Flask serves both the frontend UI and the backend API from the same origin, so
the whole app is available at one URL.

### Files for deployment

| File                    | Purpose                                        |
|-------------------------|------------------------------------------------|
| `render.yaml`           | Render Blueprint — single Python web service   |
| `backend/runtime.txt`   | Pins Python 3.12.10                            |
| `backend/requirements.txt` | Python dependencies                          |
| `frontend/index.html`   | Frontend UI served by Flask                    |
| `frontend/css/`, `frontend/js/` | Frontend static assets served by Flask |

### Steps

1. Push the repository to GitHub.
2. Go to [render.com](https://render.com) → **New +** → **Blueprint** → select the repo.
3. Render reads `render.yaml` and creates the service:
   - `marketing-email-generator` (Flask app, free web service, `rootDir: backend`)
4. Deploy. The first deploy downloads the selected model and may take several minutes.
5. Open the deployed URL and test.

### Important notes

- **Free tier memory:** Render free web services have **512 MB RAM** and are best used with a very small model such as `OuteAI/Lite-Oute-1-300M-Instruct`. Larger models may exceed this limit and fail to load.
- **Cold starts:** Free services spin down after inactivity; the first request after idle may take time while the model reloads.
- **Health check:** Render uses `GET /health` on the backend.

## Environment Variables

See [.env.example](../.env.example) at the project root.

| Variable                    | Default                            | Description                      |
|-----------------------------|------------------------------------|----------------------------------|
| `FLASK_ENV`                 | `development`                      | `development` or `production`    |
| `FLASK_DEBUG`               | `false`                            | Enable/disable debug mode        |
| `HOST`                      | `0.0.0.0`                          | Bind host                        |
| `PORT`                      | `5000`                             | Bind port (Render injects `PORT`)|
| `MODEL_NAME`                | `OuteAI/Lite-Oute-1-300M-Instruct` | Hugging Face model           |
| `MAX_NEW_TOKENS`            | `250`                              | Max tokens generated             |
| `GENERATION_TIMEOUT_SECONDS`| `300`                              | Inference timeout                |
| `MAX_REQUEST_BODY_BYTES`    | `65536`                            | Max request body size            |
| `LOAD_IN_8BIT`              | `false`                            | Load the model in 8-bit mode if supported |
| `HF_TOKEN`                  | _(optional)_                      | Hugging Face access token for authenticated model downloads |

