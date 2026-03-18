from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, DateTime, Float, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AnalysisReport(Base):
    __tablename__ = "analysis_report"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # business keys
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    job_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)

    # report meta
    report_version: Mapped[str] = mapped_column(String(20), nullable=False)

    # outputs
    overall_grade: Mapped[str | None] = mapped_column(String(5), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    volatility: Mapped[float | None] = mapped_column(Numeric(10, 4), nullable=True)

    summary: Mapped[str] = mapped_column(Text, nullable=False)

    action_items: Mapped[list[Any]] = mapped_column(JSONB, nullable=False, default=list)
    highlights: Mapped[list[Any]] = mapped_column(JSONB, nullable=False, default=list)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # platform-in-platform
    platform: Mapped[str] = mapped_column(String(32), nullable=False, default="sourcing")

    # raw signals
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    views: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sales: Mapped[int | None] = mapped_column(Integer, nullable=True)