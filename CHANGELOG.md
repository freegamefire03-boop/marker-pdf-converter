# Changelog

All notable changes to this project are logged here, newest first.

## 2026-07-21
- Fixed: Cell 1 now deletes stale `config.json`/`status.json`/`.tunnel_url` at start — wait loop always blocks for fresh config
- Fixed: Cell 8 worker subprocess warmup block removed — `patched_create_model_dict()` was hanging during model caching; models now load on first job instead
- Fixed: Added missing `/api/status` route to notebook's inline FastAPI server (Cell 4) — UI now shows live progress
- Fixed: Added Docker shim to Cell 2 — marker_single checks for docker binary at startup, fails without it on Kaggle
- Fixed: Cell 8 mode check now accepts `"single"` alongside `"default"` and `"batch_multiplier"` — matches what the UI saves

## 2026-07-21
- Added: Zero-intervention flow — Cell 4 now saves tunnel URL to `.tunnel_url`; Cell 5 waits in a loop until user configures a valid Drive link via the UI, then auto-proceeds
- Changed: Cell 5 wait loop reads saved tunnel URL and re-displays it; no need to run cells in two batches

## 2026-07-21
- Changed: Replaced ngrok with Cloudflare Tunnel (cloudflared) in Cell 4 — no API key required, uses trycloudflare.com free tunnel
- Changed: Updated Cell 4 comment and tunnel code accordingly
- Removed: All ngrok/pyngrok dependencies and NGROK_AUTH_TOKEN references
- Fixed: Cell 7 — `if/else` indentation bug that would cause SyntaxError in single-file mode
- Fixed: Cell 7 — `print()` indentation error and duplicate file listing loop in folder mode
- Fixed: Cell 10 — duplicate `write_status()` call
- Changed: Replaced Cell 4's simplified inline HTML_STR with the full `config_ui.html` — now includes real-time progress views (preparing, marker stages, download), status polling, stage pills, and progress bars
- Fixed: Cell 10 — missing `import json` that would cause NameError when falling back to config.json for GitHub token

## 2026-07-20
- Added: Standalone Gradio/HTML config UI — `config_ui.html` (pure HTML/CSS/JS, editable externally) and `gradio_config_ui.py` (FastAPI backend with save/load/reset API); dark mode toggle
- Changed: MODE now defaults to "auto" — auto-detects from link format (folder vs single-file); user can still override manually
- Changed: merged config block into Cell 4 (validation gate) — now prints a formatted summary of all settings before asking the user to confirm; Cell 5 reduced to a backward-compat comment
- Fixed: gdown installed every folder run — added try/except import guard
- Fixed: duplicate BATCH_INPUT_DIR in Cell 5 — removed redundant first assignment
- Fixed: marker-pdf installed every run — added try/except import check before pip install
- Changed: Removed unused `PLATFORM` variable
- Fixed: `shutil.rmtree` follows symlinks — added `os.path.islink` guard before removing cache
- Fixed: 3GB cache copied every run — added `.cache_ready` marker file to skip copy if already populated this session; distinguished "mounted but empty" from "not mounted" messages
