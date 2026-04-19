# Video Link Bulk Grabber

A creator-focused bulk video link grabber with a modern web dashboard.

It is built for grabbing links from creator/profile pages across:
- Redgifs (direct media links)
- VK (via yt-dlp extraction)
- Other websites supported by yt-dlp

## Features

- Auto platform detection
- Manual platform override (Redgifs, VK, Generic)
- Quality preference (`best`, `hd`, `sd`, `gif`, `poster`)
- Bulk extraction with max item control
- Export links as TXT or CSV
- Single-service deployment (FastAPI + static frontend)
- Mobile-friendly polished UI

## Preview Workflow

1. Paste creator URL.
2. Select platform (or Auto Detect).
3. Click Grab Links.
4. Copy all links or download TXT/CSV.

## Tech Stack

- Backend: FastAPI
- Extraction: Redgifs API + yt-dlp
- Frontend: Vanilla JS + custom CSS theme

## Quick Start (Windows PC)

### Step 1: Clone the Repository

```powershell
git clone https://github.com/sahanvin2/Video-Link-Bulk-Grabber.git
cd Video-Link-Bulk-Grabber
```

### Step 2: Create Virtual Environment

```powershell
python -m venv .venv
```

### Step 3: Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

**Note:** If you get a PowerShell execution policy error, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Run the Application

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 6: Open in Browser

Open your web browser and navigate to:

```
http://127.0.0.1:8000
```

You should see the **Video Link Bulk Grabber** dashboard with the ability to input creator URLs and extract links.

## API

### POST /api/grab

Request body:

```json
{
  "creator_url": "https://www.redgifs.com/users/autumnrenxo",
  "platform": "auto",
  "quality": "best",
  "max_items": 5000
}
```

Response shape:

```json
{
  "platform": "redgifs",
  "source": "autumnrenxo",
  "total": 95,
  "links": ["https://media.redgifs.com/...mp4"],
  "note": "Direct media URLs from Redgifs API."
}
```

## Platform Notes

- Redgifs: Uses official public API flow with temporary token and pagination.
- VK/Generic: Uses yt-dlp extraction. Depending on site restrictions, some results may be page URLs instead of direct media URLs.
- Login-required and anti-bot protected pages may fail without browser cookies/session.

## Testing

```powershell
pytest
```

## Deployment

### Local Development (Windows)

The Quick Start section above covers local development on Windows.

### Production Deployment

For detailed production deployment guides (Render, Railway, VPS), see:

- [DEPLOYMENT.md](DEPLOYMENT.md)

### Deploy on Render (Recommended)

1. Push this repository to GitHub
2. Go to [Render.com](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Set:
   - **Runtime:** Python 3
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Click Deploy

Your app will be live at a public URL provided by Render.

### Deploy on Railway

1. Go to [Railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Railway auto-detects Python
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Deploy

## System Requirements

- **Python:** 3.10 or higher
- **OS:** Windows, macOS, or Linux
- **RAM:** 256MB minimum
- **Disk:** ~100MB for dependencies

## Troubleshooting

### Port 8000 Already in Use

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

Change `8000` to any available port (8001, 8002, etc.)

### Virtual Environment Activation Issues

If `.\.venv\Scripts\Activate.ps1` fails, try:

```powershell
.\.venv\Scripts\Activate.bat
```

Or use:

```powershell
python -m venv .venv --upgrade-deps
.\.venv\Scripts\Activate.ps1
```

### Module Not Found Errors

Ensure virtual environment is activated, then reinstall:

```powershell
pip install --upgrade -r requirements.txt
```

## Support

For issues or feature requests, please open an issue on GitHub.

## GitHub Publish

Suggested GitHub repository description:

> Creator-focused bulk video link grabber with a modern FastAPI web UI, Redgifs direct-link support, and yt-dlp-based extraction for VK and other supported platforms.

To publish your local changes:

```powershell
git status
git add .
git commit -m "Build multi-platform bulk link grabber"
git branch -M main
git remote add origin https://github.com/sahanvin2/Video-Link-Bulk-Grabber.git
git push -u origin main
```

If `origin` already exists, skip the `git remote add origin` line.

## Important Disclaimer

Use this project only for legal content and where you have rights/permission to access and process links. Respect each platform's Terms of Service and local laws.
