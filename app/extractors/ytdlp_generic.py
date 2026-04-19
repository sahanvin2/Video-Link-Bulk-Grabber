from __future__ import annotations

from urllib.parse import urlparse

from yt_dlp import YoutubeDL

from .base import BaseExtractor, ExtractResult, ExtractorError


class YtDlpExtractor(BaseExtractor):
    platform_name = "generic"

    def __init__(self, platform_name: str = "generic") -> None:
        self.platform_name = platform_name

    def can_handle(self, source: str) -> bool:
        return source.startswith("http://") or source.startswith("https://")

    def _candidate_from_item(self, item: dict, quality: str) -> str | None:
        if quality == "best":
            for key in ("url", "webpage_url", "original_url"):
                value = item.get(key)
                if isinstance(value, str) and value.startswith("http"):
                    return value
        else:
            formats = item.get("formats") or []
            ranked = []
            for fmt in formats:
                ext = (fmt.get("ext") or "").lower()
                url = fmt.get("url")
                if not isinstance(url, str) or not url.startswith("http"):
                    continue
                if quality in ("hd", "sd") and ext in ("mp4", "mkv", "webm"):
                    height = fmt.get("height") or 0
                    ranked.append((int(height), url))
                elif quality == "gif" and ext == "gif":
                    ranked.append((1, url))
                elif quality == "poster" and ext in ("jpg", "jpeg", "png", "webp"):
                    ranked.append((1, url))
            if ranked:
                ranked.sort(key=lambda x: x[0], reverse=True)
                return ranked[0][1]

        for key in ("url", "webpage_url", "original_url"):
            value = item.get(key)
            if isinstance(value, str) and value.startswith("http"):
                return value
        return None

    def _walk(self, node: dict, quality: str, links: list[str], seen: set[str], max_items: int) -> None:
        entries = node.get("entries")
        if isinstance(entries, list):
            for sub in entries:
                if not isinstance(sub, dict):
                    continue
                self._walk(sub, quality, links, seen, max_items)
                if len(links) >= max_items:
                    return

        candidate = self._candidate_from_item(node, quality)
        if candidate and candidate not in seen and len(links) < max_items:
            seen.add(candidate)
            links.append(candidate)

    def extract(self, source: str, quality: str, max_items: int) -> ExtractResult:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": False,
            "ignoreerrors": True,
            "socket_timeout": 35,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(source, download=False)
        except Exception as exc:  # noqa: BLE001
            raise ExtractorError(f"Extraction failed for URL: {exc}") from exc

        if not isinstance(info, dict):
            raise ExtractorError("Unable to parse source as a supported creator page.")

        links: list[str] = []
        seen: set[str] = set()
        self._walk(info, quality, links, seen, max_items)

        if not links:
            raise ExtractorError(
                "No videos found. This site may require login, anti-bot clearance, or unsupported creator layout."
            )

        host = urlparse(source).netloc
        note = "Collected links via yt-dlp. Some platforms may return page URLs instead of direct media URLs."
        return ExtractResult(platform=self.platform_name, source=host, links=links, note=note)
