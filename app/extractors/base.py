from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExtractResult:
    platform: str
    source: str
    links: list[str]
    note: str | None = None


class ExtractorError(RuntimeError):
    pass


class BaseExtractor:
    platform_name: str = "generic"

    def can_handle(self, source: str) -> bool:
        raise NotImplementedError

    def extract(self, source: str, quality: str, max_items: int) -> ExtractResult:
        raise NotImplementedError
