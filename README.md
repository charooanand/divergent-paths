# Earnings Apps (Render-ready)

Two Plotly Dash apps served behind one Flask server on Render.

## Structure
- `/rank/` → Earnings Rank Gap
- `/level/` → Earnings Level Gap

## Local run
```bash
pip install -r requirements.txt
export PORT=8000
python multi.py
# or with gunicorn
gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT multi:server
```

## Deploy on Render
- Connect this repo
- Render auto-detects `render.yaml`
- Start command: `gunicorn -w 2 -k gthread -b 0.0.0.0:$PORT multi:server`
