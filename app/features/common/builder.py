import math


def build_features(data):

    price = data["price"]
    views = data["views"]

    log_price = math.log(price + 1)
    view_score = min(views / 1000, 1)

    demand = view_score * 100
    price_level = price / 10000
    risk = 1 if price > 30000 else 0

    return {
        "price": price,
        "views": views,
        "log_price": log_price,
        "view_score": view_score,
        "demand_index": demand,
        "price_level": price_level,
        "risk_price": risk
    }
