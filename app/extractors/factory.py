from __future__ import annotations

from urllib.parse import urlparse

from .base import BaseExtractor, ExtractorError
from .redgifs import RedgifsExtractor
from .ytdlp_generic import YtDlpExtractor


def detect_platform(source: str) -> str:
    lower = source.lower()
    if "redgifs.com" in lower:
        return "redgifs"
    if "vk.com" in lower or "vkvideo.ru" in lower:
        return "vk"
    return "generic"


def get_extractor(source: str, platform: str) -> BaseExtractor:
    selected = platform
    if selected == "auto":
        selected = detect_platform(source)

    if selected == "redgifs":
        return RedgifsExtractor()
    if selected == "vk":
        return YtDlpExtractor(platform_name="vk")
    if selected == "generic":
        return YtDlpExtractor(platform_name="generic")

    raise ExtractorError(f"Unsupported platform selector: {platform}")
