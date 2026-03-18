from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, String, Text, func

from app.core.database import Base


class PredictResult(Base):

    __tablename__ = "predict_result"

    id = Column(BigInteger, primary_key=True, index=True)

    platform = Column(String(32), nullable=False)

    product_id = Column(BigInteger, nullable=False)

    price = Column(Float, nullable=True)

    views = Column(Integer, nullable=True)

    sales = Column(Integer, nullable=True)

    score = Column(Float, nullable=False)

    grade = Column(String(5), nullable=False)

    comment = Column(Text, nullable=True)

    ml_prediction = Column(Float, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )