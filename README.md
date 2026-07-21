# Marker PDF Converter

Converts PDFs to Markdown using the Marker library on Kaggle, with multi-GPU support and optional GitHub push.

## Status
Active development

## Features
- Single PDF or folder batch processing
- Multi-GPU split mode for large PDFs
- Persistent model cache via Kaggle Dataset (avoids re-download)
- Auto-merge split PDF outputs
- Optional GitHub push of output zips

## Tech Stack
- Python, Marker, PyTorch
- Kaggle Notebooks (target platform)

## Setup / Run
1. Add the `marker-model-cache` dataset to your Kaggle notebook
2. Enable **Internet** and **GPU** in Kaggle notebook settings
3. Set `DRIVE_LINK` or `DRIVE_FOLDER_LINK` via the config UI or in Cell 4
4. Run all cells
5. The config UI is accessible via the Cloudflare Tunnel URL printed by Cell 4

## Known Issues / TODO
