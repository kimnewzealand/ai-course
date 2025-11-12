# Web API MVP

## Setup
1. Install uv: `pip install uv`
2. Create virtual environment: `uv venv`
3. Activate: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
4. Install dependencies: `uv pip install -r requirements.txt`

## Run
uvicorn app.main:app --reload

## Test
pytest

## API Docs
http://localhost:8000/docs
