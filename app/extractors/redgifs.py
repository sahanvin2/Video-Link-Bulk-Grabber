from __future__ import annotations

import re
import time
from urllib.parse import urlencode, urlparse

import httpx

from .base import BaseExtractor, ExtractResult, ExtractorError

API_BASE = "https://api.redgifs.com/v2"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.redgifs.com/",
    "Origin": "https://www.redgifs.com",
}


class RedgifsExtractor(BaseExtractor):
    platform_name = "redgifs"

    def can_handle(self, source: str) -> bool:
        return "redgifs.com" in source.lower() or re.fullmatch(r"[a-zA-Z0-9_\-.]+", source) is not None

    def _parse_username(self, source: str) -> str:
        source = source.strip()
        if not source:
            raise ExtractorError("Creator URL or username is empty.")
        if "://" not in source:
            return source.strip("/")
        parsed = urlparse(source)
        path = parsed.path.strip("/")
        m = re.match(r"users/([^/]+)", path, flags=re.IGNORECASE)
        if not m:
            raise ExtractorError("Invalid Redgifs creator URL. Use https://www.redgifs.com/users/<username>")
        return m.group(1)

    def _get_temp_token(self, client: httpx.Client) -> str:
        r = client.get(f"{API_BASE}/auth/temporary", headers=DEFAULT_HEADERS, timeout=30)
        r.raise_for_status()
        token = r.json().get("token")
        if not token:
            raise ExtractorError("Unable to get Redgifs API token.")
        return token

    def _pick(self, gif_obj: dict, quality: str) -> str | None:
        urls = gif_obj.get("urls") or {}
        order = {
            "hd": ["hd", "sd", "gif", "poster"],
            "sd": ["sd", "hd", "gif", "poster"],
            "gif": ["gif", "hd", "sd", "poster"],
            "poster": ["poster", "hd", "sd", "gif"],
            "best": ["hd", "sd", "gif", "poster"],
        }.get(quality, ["hd", "sd", "gif", "poster"])
        for key in order:
            value = urls.get(key)
            if value:
                return value
        return None

    def extract(self, source: str, quality: str, max_items: int) -> ExtractResult:
        username = self._parse_username(source)
        links: list[str] = []
        seen: set[str] = set()

        with httpx.Client(follow_redirects=True, headers=DEFAULT_HEADERS) as client:
            token = self._get_temp_token(client)
            auth_headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {token}"}
            page = 1
            cursor: str | None = None

            while len(links) < max_items:
                params = {"order": "recent", "count": "100", "page": str(page)}
                if cursor:
                    params["cursor"] = cursor
                url = f"{API_BASE}/users/{username}/search?{urlencode(params)}"

                try:
                    res = client.get(url, headers=auth_headers, timeout=40)
                    if res.status_code in (401, 403):
                        token = self._get_temp_token(client)
                        auth_headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {token}"}
                        res = client.get(url, headers=auth_headers, timeout=40)
                    res.raise_for_status()
                except httpx.HTTPError as exc:
                    raise ExtractorError(f"Redgifs request failed: {exc}") from exc

                data = res.json()
                gifs = data.get("gifs") or []
                if not gifs:
                    break

                for gif_obj in gifs:
                    media_url = self._pick(gif_obj, quality)
                    if media_url and media_url not in seen:
                        seen.add(media_url)
                        links.append(media_url)
                        if len(links) >= max_items:
                            break

                next_cursor = data.get("cursor") or data.get("next")
                if next_cursor and next_cursor != cursor:
                    cursor = next_cursor
                    page += 1
                elif len(gifs) < 100:
                    break
                else:
                    page += 1
                time.sleep(0.15)

        return ExtractResult(
            platform=self.platform_name,
            source=username,
            links=links,
            note="Direct media URLs from Redgifs API.",
        )
