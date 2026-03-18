from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.deps import get_db
from app.models.analysis_report import AnalysisReport
from app.core.security import require_api_key

router = APIRouter(prefix="/api/analyze", tags=["Analyze"])


# ----------------------
# KPI Summary
# ----------------------
@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    """
    KPI 요약 정보 반환
    total_reports: 총 리포트 수
    total_sales: 총 판매량 합계
    avg_confidence: 평균 confidence
    avg_price: 평균 가격
    """
    try:
        total_reports = db.query(func.count(AnalysisReport.id)).scalar() or 0
        total_sales = db.query(func.sum(AnalysisReport.sales)).scalar() or 0
        avg_confidence = db.query(func.avg(AnalysisReport.confidence)).scalar() or 0
        avg_price = db.query(func.avg(AnalysisReport.price)).scalar() or 0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB 조회 실패: {str(e)}")

    return {
        "total_reports": int(total_reports),
        "total_sales": int(total_sales),
        "avg_confidence": round(float(avg_confidence), 4) if avg_confidence else 0.0,
        "avg_price": round(float(avg_price), 2) if avg_price else 0.0
    }


# ----------------------
# Recent Activity Feed
# ----------------------
@router.get("/activity")
def get_activity(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    """
    최근 Activity Feed 반환 (limit 기본 20, 최대 100)
    """
    try:
        reports = (
            db.query(AnalysisReport)
            .order_by(AnalysisReport.created_at.desc())
            .limit(limit)
            .all()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB 조회 실패: {str(e)}")

    activity_list = [
        {
            "id": r.id,
            "platform": r.platform,
            "product_id": r.product_id,
            "job_id": r.job_id,
            "report_version": r.report_version,
            "overall_grade": r.overall_grade,
            "confidence": float(r.confidence) if r.confidence is not None else None,
            "volatility": float(r.volatility) if r.volatility is not None else None,
            "summary": r.summary,
            "sales": r.sales,
            "price": r.price,
            "views": r.views,
            "action_items": r.action_items,
            "highlights": r.highlights,
            "created_at": r.created_at.isoformat()
        }
        for r in reports
    ]

    return activity_list