from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote

import requests
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
GENERATED_DIR = STATIC_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")

POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt/"


def fetch_generated_image(prompt: str) -> bytes:
    """Fetches an image from a free text-to-image endpoint."""
    safe_prompt = quote(prompt.strip())
    image_url = (
        f"{POLLINATIONS_BASE_URL}{safe_prompt}"
        "?width=768&height=768&nologo=true&enhance=true"
    )

    response = requests.get(image_url, timeout=60)
    response.raise_for_status()
    return response.content


@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.post("/api/generate")
def generate_image():
    payload = request.get_json(silent=True) or {}
    prompt = (payload.get("prompt") or "").strip()

    if len(prompt) < 3:
        return jsonify({"error": "Prompt must be at least 3 characters."}), 400

    try:
        image_data = fetch_generated_image(prompt)
    except requests.RequestException as exc:
        return (
            jsonify(
                {
                    "error": "Image generation service is unavailable right now.",
                    "details": str(exc),
                }
            ),
            502,
        )

    filename = f"image_{abs(hash(prompt)) % 10**12}.png"
    image_path = GENERATED_DIR / filename
    image_path.write_bytes(image_data)

    return jsonify({"imageUrl": f"/generated/{filename}", "prompt": prompt})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
