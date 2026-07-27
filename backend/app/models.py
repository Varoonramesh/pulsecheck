from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class URLMonitor(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String, unique=True, nullable=False)

    status = Column(String, default="UNKNOWN")

    status_code = Column(Integer, nullable=True)

    response_time_ms = Column(Float, nullable=True)

    checked_at = Column(DateTime, default=datetime.utcnow)
