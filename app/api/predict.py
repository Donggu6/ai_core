from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.deps import get_db, settings
from app.models.predict_result import PredictResult
from app.services.scoring import score as score_fn, PLATFORMS
from app.services.ml_model import ModelService
from app.core.security import require_api_key

router = APIRouter(prefix="/api/predict", tags=["Predict"])

# Settings & ML 모델 초기화
_settings = settings()
_model = ModelService(_settings.model_path)
_model.load()

# require_api_key가 str | None 을 받도록 맞춤
_API_KEY = getattr(_settings, "api_key", None)


class PredictRequest(BaseModel):
    platform: str = Field(
        default=_settings.default_platform,
        description=f"platform module ({', '.join(PLATFORMS.keys())})",
    )
    product_id: int = Field(0, description="Internal product ID")
    price: int = Field(..., ge=0, description="Product price")
    views: int = Field(..., ge=0, description="Number of views")
    sales: int = Field(..., ge=0, description="Number of sales")

    @field_validator("platform")
    @classmethod
    def validate_platform(cls, v: str) -> str:
        v_norm = v.lower().strip()
        if v_norm not in PLATFORMS:
            raise ValueError(
                f"Unsupported platform: {v_norm}. Allowed: {', '.join(PLATFORMS.keys())}"
            )
        return v_norm


class PredictResponse(BaseModel):
    id: int
    platform: str
    product_id: int
    score: float
    grade: str
    comment: str
    ml_prediction: float | None = None
    saved: bool = True


@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest, db: Session = Depends(get_db)) -> PredictResponse:
    require_api_key(_API_KEY)

    # 점수 계산
    s = score_fn(req.platform, req.price, req.views, req.sales)

    # ML 예측
    ml_pred = _model.predict(req.price, req.views, req.sales)

    # DB 저장
    row = PredictResult(
        platform=req.platform,
        product_id=int(req.product_id),
        price=float(req.price),
        views=int(req.views),
        sales=int(req.sales),
        score=float(s.score),
        grade=str(s.grade),
        comment=str(s.comment),
        ml_prediction=float(ml_pred) if ml_pred is not None else None,
    )

    row_id = 0
    saved = False

    try:
        db.add(row)
        db.commit()
        db.refresh(row)

        _id_value = getattr(row, "id", None)
        row_id = int(_id_value) if _id_value is not None else 0
        saved = True

    except Exception:
        db.rollback()
        row_id = 0
        saved = False

    return PredictResponse(
        id=row_id,
        platform=req.platform,
        product_id=int(req.product_id),
        score=float(s.score),
        grade=str(s.grade),
        comment=str(s.comment),
        ml_prediction=float(ml_pred) if ml_pred is not None else None,
        saved=saved,
    )


@router.post("/{platform}/predict", response_model=PredictResponse)
def predict_for_platform(
    platform: str,
    req: PredictRequest,
    db: Session = Depends(get_db),
) -> PredictResponse:
    """
    /api/predict/sourcing/predict, /api/predict/consignment/predict 등 편의용
    """
    req.platform = platform
    return predict(req, db)


@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    """
    최근 12개월 Revenue / Session 차트 데이터
    """
    require_api_key(_API_KEY)

    today = datetime.utcnow()
    chart_data = []

    for i in range(11, -1, -1):
        month_start = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        next_month = (month_start + timedelta(days=32)).replace(day=1)

        revenue = (
            db.query(func.sum(PredictResult.price))
            .filter(
                PredictResult.created_at >= month_start,
                PredictResult.created_at < next_month,
            )
            .scalar()
            or 0
        )

        sessions = (
            db.query(func.count(PredictResult.id))
            .filter(
                PredictResult.created_at >= month_start,
                PredictResult.created_at < next_month,
            )
            .scalar()
            or 0
        )

        chart_data.append(
            {
                "month": month_start.strftime("%Y-%m"),
                "revenue": float(revenue),
                "sessions": int(sessions),
            }
        )

    return chart_data