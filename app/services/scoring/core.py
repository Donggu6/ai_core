# scoring.py
from dataclasses import dataclass

PLATFORMS = {
    # platform-in-platform: each module can have different weights/logic
    "sourcing":     {"w_views": 0.45, "w_sales": 2.2, "w_price": 0.00010},
    "consignment":  {"w_views": 0.35, "w_sales": 2.5, "w_price": 0.00008},
    "overseas":     {"w_views": 0.40, "w_sales": 2.0, "w_price": 0.00012},
    "vertical":     {"w_views": 0.50, "w_sales": 1.8, "w_price": 0.00009},
    "store":        {"w_views": 0.42, "w_sales": 2.1, "w_price": 0.00011},
}

@dataclass(frozen=True)
class ScoreResult:
    score: float
    grade: str
    comment: str

def score(platform: str, price: int, views: int, sales: int) -> ScoreResult:
    p = (platform or "sourcing").lower().strip()
    weights = PLATFORMS.get(p, PLATFORMS["sourcing"])

    raw = (views * weights["w_views"]) + (sales * weights["w_sales"]) - (price * weights["w_price"])
    # normalize-ish into 0..100 band for UI
    score_val = max(0.0, min(100.0, raw))

    grade = "A" if score_val >= 80 else "B" if score_val >= 50 else "C"
    comment = {
        "A": "매우 우수: 확장/자동화 추천",
        "B": "양호: 개선 여지 있음",
        "C": "주의: 가격/전환 개선 필요",
    }[grade]

    return ScoreResult(score=round(score_val, 2), grade=grade, comment=comment)
