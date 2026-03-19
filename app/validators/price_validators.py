from decimal import Decimal, InvalidOperation

from app.exceptions import ValidationError

def validate_scraped_price(price):
    if price is None:
        raise ValidationError("Could not scrape product price")
    
    if isinstance(price, str):
        price = price.replace(".", "").replace(",", ".")

    try:
        price = Decimal(price)
    except (TypeError, InvalidOperation):
        raise ValidationError("Scraped price is invalid")

    if price <= 0:
        raise ValidationError("Scraped price must be greater than 0")

    return price.quantize(Decimal("0.01"))


    
def validate_price_fields(fields):
    ALLOWED_FIELDS = {"current", "average", "lowest", "highest", "total", "variation_percent", "is_best_price", "last_30_days_average", "price_trend" }

    if not fields:
        return sorted(ALLOWED_FIELDS)
    
    requested = [f.strip() for f in fields.split(",") if f.strip()]
    
    invalid_fields = [f for f in requested if f not in ALLOWED_FIELDS]

    if invalid_fields:
        raise ValidationError(
            f"Invalid stats fields: {', '.join(invalid_fields)}"
        )

    return list(dict.fromkeys(requested))