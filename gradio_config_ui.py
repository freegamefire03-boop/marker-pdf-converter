"""
Marker PDF Converter — Config Backend
Serves config_ui.html and exposes API endpoints.
Edit config_ui.html freely — the backend only handles data.
"""

import json, os, uvicorn
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Marker PDF Converter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HERE = os.path.dirname(os.path.abspath(__file__))

# Config and download paths — works on Kaggle and locally
if os.path.isdir("/kaggle/working"):
    CONFIG_DIR = "/kaggle/working"
else:
    CONFIG_DIR = HERE

CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
DOWNLOAD_DIR = CONFIG_DIR

DEFAULTS = {
    "mode": "single",
    "split_at_page": 12,
    "batch_input_dir": "/kaggle/working/pdf_batch",
    "drive_link": "",
    "drive_folder_link": "",
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
        # Migrate old mode values
        if cfg.get("mode") in ("auto", "default"):
            cfg["mode"] = "single"
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

    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

    # Set env vars for subsequent notebook cells
    if cfg.get("github_token"):
        os.environ["GITHUB_TOKEN"] = cfg["github_token"]
    if "local_cache" not in cfg:
        local_cache = os.path.join(CONFIG_DIR, "marker_models_cache")
        os.environ["HF_HOME"] = local_cache
        os.environ["TRANSFORMERS_CACHE"] = os.path.join(local_cache, "transformers")
        os.environ["TORCH_HOME"] = os.path.join(local_cache, "torch")
        os.environ["XDG_CACHE_HOME"] = local_cache

    lines = "\n".join(f"  {k} = {v!r}" for k, v in cfg.items())
    return {"status": "ok", "message": f"Config saved.\n\n{lines}"}


@app.post("/api/reset")
async def reset():
    return DEFAULTS


# ── File downloads ─────────────────────────────────────────────────────────

def human_size(path):
    b = os.path.getsize(path)
    for unit in ("B", "KB", "MB", "GB"):
        if b < 1024:
            return f"{b:.0f} {unit}"
        b /= 1024
    return f"{b:.1f} GB"


@app.get("/api/files")
async def list_files():
    try:
        files = []
        for p in sorted(Path(DOWNLOAD_DIR).iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if p.suffix.lower() in (".zip", ".md", ".txt", ".pdf", ".json") and p.is_file():
                files.append({
                    "name": p.name,
                    "size": human_size(p),
                })
        return {"files": files}
    except Exception as e:
        return {"files": [], "error": str(e)}


@app.get("/api/download/{filename:path}")
async def download_file(filename: str):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.isfile(filepath):
        return HTMLResponse("File not found", status_code=404)
    return FileResponse(filepath, filename=filename)


# ── Main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    PORT = 7862
    print(f"UI running at http://127.0.0.1:{PORT}")
    print("Edit config_ui.html to customize the look.")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
