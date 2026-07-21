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
3. Upload the notebook, attach the dataset, start a GPU session
4. **Run all cells** — the notebook starts a config UI (accessible via the Cloudflare Tunnel URL) and waits for you to configure settings
5. Open the tunnel URL, configure your Drive link and options, click **Save & Apply**
6. Processing starts automatically — no need to run cells in batches

## Known Issues / TODO
