from datetime import datetime, timedelta
from sqlalchemy import func
from app.models.price_history_model import PriceHistory
from app.db import db


def to_number(value):
    if value is None:
        return None
    return round(float(value), 2)


def calculate_stats(prices_query, requested_fields):
    stats = {}

    first_record = prices_query.first()
    product_id = first_record.product_id if first_record else None

    # CURRENT
    if "current" in requested_fields:
        latest_price = (
            prices_query.order_by(PriceHistory.collected_at.desc())
            .with_entities(PriceHistory.price)
            .first()
        )
        stats["current"] = to_number(latest_price[0]) if latest_price else None

    # AGGREGATES
    aggregate_fields = ["average", "lowest", "highest", "total"]
    if product_id and any(f in requested_fields for f in aggregate_fields):
        aggregates = db.session.query(
            func.avg(PriceHistory.price),
            func.min(PriceHistory.price),
            func.max(PriceHistory.price),
            func.count(PriceHistory.id)
        ).filter_by(product_id=product_id).first()

        avg, lowest, highest, total = aggregates

        if "average" in requested_fields:
            stats["average"] = to_number(avg)
        if "lowest" in requested_fields:
            stats["lowest"] = to_number(lowest)
        if "highest" in requested_fields:
            stats["highest"] = to_number(highest)
        if "total" in requested_fields:
            stats["total"] = total

    # VARIATION_PERCENT
    if "variation_percent" in requested_fields:
        first_price = (
            prices_query.order_by(PriceHistory.collected_at.asc())
            .with_entities(PriceHistory.price)
            .first()
        )
        latest_price = (
            prices_query.order_by(PriceHistory.collected_at.desc())
            .with_entities(PriceHistory.price)
            .first()
        )

        if first_price and latest_price and first_price[0] != 0:
            variation = ((latest_price[0] - first_price[0]) / first_price[0]) * 100
            stats["variation_percent"] = to_number(variation)
        else:
            stats["variation_percent"] = None

    # IS_BEST_PRICE
    if "is_best_price" in requested_fields and product_id:
        latest_price = (
            prices_query.order_by(PriceHistory.collected_at.desc())
            .with_entities(PriceHistory.price)
            .first()
        )
        lowest_price = (
            db.session.query(func.min(PriceHistory.price))
            .filter_by(product_id=product_id)
            .scalar()
        )
        stats["is_best_price"] = latest_price[0] == lowest_price if latest_price else False

    # LAST_30_DAYS_AVERAGE
    if "last_30_days_average" in requested_fields and product_id:
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        last_30_avg = (
            db.session.query(func.avg(PriceHistory.price))
            .filter(
                PriceHistory.product_id == product_id,
                PriceHistory.collected_at >= thirty_days_ago
            )
            .scalar()
        )
        stats["last_30_days_average"] = to_number(last_30_avg)

    # PRICE_TREND
    if "price_trend" in requested_fields:
        first_price = (
            prices_query.order_by(PriceHistory.collected_at.asc())
            .with_entities(PriceHistory.price)
            .first()
        )
        latest_price = (
            prices_query.order_by(PriceHistory.collected_at.desc())
            .with_entities(PriceHistory.price)
            .first()
        )
        if first_price and latest_price:
            if latest_price[0] > first_price[0]:
                stats["price_trend"] = "up"
            elif latest_price[0] < first_price[0]:
                stats["price_trend"] = "down"
            else:
                stats["price_trend"] = "stable"
        else:
            stats["price_trend"] = None

    return stats