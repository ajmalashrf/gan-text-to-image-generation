# GAN Text-to-Image Generation

A simple full-stack text-to-image project with:

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask API
- **Generation Flow:** User prompt → backend endpoint → generated image shown in UI

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## API

`POST /api/generate`

Request body:

```json
{
  "prompt": "a cyberpunk owl in neon rain"
}
```

Response:

```json
{
  "imageUrl": "/generated/image_123456.png",
  "prompt": "a cyberpunk owl in neon rain"
}
```
