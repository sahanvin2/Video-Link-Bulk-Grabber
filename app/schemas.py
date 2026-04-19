from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, HttpUrl


class GrabRequest(BaseModel):
    creator_url: str = Field(min_length=3, description="Creator profile URL or username")
    platform: Literal["auto", "redgifs", "vk", "generic"] = "auto"
    quality: Literal["hd", "sd", "gif", "poster", "best"] = "best"
    max_items: int = Field(default=5000, ge=1, le=50000)


class GrabResponse(BaseModel):
    platform: str
    source: str
    total: int
    links: list[str]
    note: Optional[str] = None
