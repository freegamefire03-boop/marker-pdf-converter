# Changelog

All notable changes to this project are logged here, newest first.

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
