import math


class ProductScorer:

    @staticmethod
    def score(features):

        score = 0

        score += features["demand_index"] * 40
        score += (1 - features["risk_price"]) * 30
        score += features["price_level"] * 20
        score += features["view_score"] * 10

        total = round(score, 1)

        if total >= 80:
            grade = "A"
        elif total >= 60:
            grade = "B"
        elif total >= 40:
            grade = "C"
        else:
            grade = "D"

        return {
            "total_score": total,
            "grade": grade
        }


class Product:
    pass
