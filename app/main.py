from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.extractors.base import ExtractorError
from app.extractors.factory import get_extractor
from app.schemas import GrabRequest, GrabResponse

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Video Link Bulk Grabber", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def web_root() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/grab", response_model=GrabResponse)
async def grab_links(payload: GrabRequest) -> GrabResponse:
    try:
        extractor = get_extractor(payload.creator_url, payload.platform)
        result = await run_in_threadpool(
            extractor.extract,
            payload.creator_url,
            payload.quality,
            payload.max_items,
        )
    except ExtractorError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Unexpected error: {exc}") from exc

    return GrabResponse(
        platform=result.platform,
        source=result.source,
        total=len(result.links),
        links=result.links,
        note=result.note,
    )
