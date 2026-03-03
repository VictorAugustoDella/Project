from app.exceptions import ValidationError

def _validate_price_format(price_format):
    if price_format is None:
        raise ValidationError("Price is required")
    
    if not isinstance(price_format, (int, float)):
        raise ValidationError("Price must be a number")
        
    if price_format <= 0:
        raise ValidationError("Price must be greater than 0")
    
    return float(price_format)

def validate_price(data):
    if not data:  
        raise ValidationError("Missing data")
    
    price = _validate_price_format(data.get("price"))
    
    return {
        'price': price
    }
    
def validate_price_fields(fields):
    ALLOWED_FIELDS = {"current", "average", "lowest", "highest", "total", "variation_percent", "is_best_price", "last_30_days_average", "price_trend" }

    if not fields:
        return list(ALLOWED_FIELDS)
    
    requested = fields.split(",")

    for fields in requested:
        if fields not in ALLOWED_FIELDS:
            raise ValidationError(f"Invalid stats fields: {fields}")

    return requested