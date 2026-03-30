from __future__ import annotations

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    limit: int = Field(..., ge=1)
    offset: int = Field(..., ge=0)
    total: int = Field(..., ge=0)


class ErrorResponse(BaseModel):
    code: int
    detail: str
    request_path: str
    timestamp: datetime


class TimeStampedResponse(BaseModel):
    created_at: datetime


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    pagination: PaginationMeta