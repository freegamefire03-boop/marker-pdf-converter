"""
Marker PDF Converter — Config Backend
Serves config_ui.html and exposes API endpoints.
Edit config_ui.html freely — the backend only handles data.
"""

import json, os, uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Marker PDF Converter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = "/kaggle/working/config.json"

DEFAULTS = {
    "mode": "auto",
    "split_at_page": 12,
    "batch_input_dir": "/kaggle/working/pdf_batch",
    "drive_link": "",
    "drive_folder_link": "https://drive.google.com/drive/folders/1Ke8QpXvI2iVkSHunL6NtKMO6ShZPd9ce?usp=drive_link",
    "zip_name": "output",
    "add_page_markers": False,
    "github_token": "",
}


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            saved = json.load(f)
        cfg = DEFAULTS.copy()
        cfg.update({k: v for k, v in saved.items() if k in DEFAULTS})
        return cfg
    return dict(DEFAULTS)


# ── Routes ────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index():
    with open(os.path.join(HERE, "config_ui.html"), encoding="utf-8") as f:
        return f.read()


@app.get("/api/load")
async def load():
    return load_config()


@app.post("/api/save")
async def save(request: Request):
    body = await request.json()
    # Handle both direct JSON and Gradio-wrapped format
    if "data" in body and isinstance(body["data"], list):
        values = body["data"][0]
    else:
        values = body

    cfg = DEFAULTS.copy()
    cfg.update({k: v for k, v in values.items() if k in DEFAULTS})

    os.makedirs(os.path.dirname(CONFIG_PATH) or ".", exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

    # Set env vars for subsequent notebook cells
    if cfg.get("github_token"):
        os.environ["GITHUB_TOKEN"] = cfg["github_token"]
    if "local_cache" not in cfg:
        local_cache = "/kaggle/working/marker_models_cache"
        os.environ["HF_HOME"] = local_cache
        os.environ["TRANSFORMERS_CACHE"] = os.path.join(local_cache, "transformers")
        os.environ["TORCH_HOME"] = os.path.join(local_cache, "torch")
        os.environ["XDG_CACHE_HOME"] = local_cache

    lines = "\n".join(f"  {k} = {v!r}" for k, v in cfg.items())
    return {"status": "ok", "message": f"Config saved.\n\n{lines}"}


@app.post("/api/reset")
async def reset():
    return DEFAULTS


# ── Main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    PORT = 7862
    print(f"UI running at http://127.0.0.1:{PORT}")
    print("Edit config_ui.html to customize the look.")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
