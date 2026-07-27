from pydantic import BaseModel, HttpUrl
from datetime import datetime


class URLCreate(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    id: int
    url: str
    status: str
    status_code: int | None
    response_time_ms: float | None
    checked_at: datetime

    class Config:
        from_attributes = True
