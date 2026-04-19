# Deployment Guide (Step by Step)

This app is a FastAPI backend + static frontend in one service.

## 1) Local Setup

1. Install Python 3.10+.
2. Open terminal in repository root.
3. Create virtual environment:
   - Windows PowerShell:
     - `python -m venv .venv`
     - `.\.venv\Scripts\Activate.ps1`
4. Install dependencies:
   - `pip install -r requirements.txt`
5. Run app:
   - `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
6. Open browser:
   - `http://127.0.0.1:8000`

## 2) Deploy on Render (Easy)

1. Push repository to GitHub.
2. Go to Render and create a new Web Service from this repo.
3. Runtime: Python 3.
4. Build command:
   - `pip install -r requirements.txt`
5. Start command:
   - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Deploy and open your Render URL.

## 3) Deploy on Railway

1. Create new project from GitHub repo.
2. Railway detects Python automatically.
3. Set start command:
   - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Deploy.

## 4) Deploy on a VPS (Ubuntu + Nginx)

1. Install python, venv, nginx.
2. Clone repo into `/opt/video-link-bulk-grabber`.
3. Create venv and install requirements.
4. Create systemd service:

```ini
[Unit]
Description=Video Link Bulk Grabber
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/video-link-bulk-grabber
ExecStart=/opt/video-link-bulk-grabber/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

5. Configure nginx reverse proxy to `127.0.0.1:8000`.
6. Enable HTTPS with certbot.

## 5) Notes

- Some websites require login/cookies/anti-bot clearance and may not return links without session context.
- Redgifs extractor returns direct media links when available.
- Generic and VK extraction rely on yt-dlp compatibility and page accessibility.
