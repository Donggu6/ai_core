from sqlalchemy import Column, BigInteger, Integer, Text, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.core.database import Base


class AiAnalysisResult(Base):

    __tablename__ = "ai_analysis_result"

    id = Column(BigInteger, primary_key=True)

    user_id = Column(BigInteger, nullable=False)
    product_id = Column(BigInteger, nullable=False)

    score = Column(Integer, nullable=False)
    report = Column(Text, nullable=False)

    features = Column(JSONB)

    model_version = Column(String(50), nullable=False, default="v0")

    created_at = Column(DateTime, server_default=func.now())
