from app.models.product_model import Product
from app.models.price_history_model import PriceHistory
from app.db import db
from app.routes.product.product_validators import NotFoundError
from app.routes.price.price_validators import validate_price, validate_price_fields
from app.services.price_stats import calculate_stats


def calculate_average(product):
    prices = [p.price for p in product.prices]
    if not prices:
        return None
    return sum(prices) / len(prices)

def calculate_current(product):
    prices = [p.price for p in product.prices]
    if not prices:
        return None
    return product.order_by(PriceHistory.collected_at.desc()).first()

def view_product_prices_by_id_service(user_id: int, id: int):
    product = Product.query.filter_by(id=id, user_id=user_id).first()
    
    if not product:
        raise NotFoundError("product not found")
    
    prices = PriceHistory.query.filter_by(product_id=id).order_by(PriceHistory.collected_at.desc()).all()
    
    return prices

def add_product_prices_by_id_service(user_id: int, id:int, data):
    validated_price = validate_price(data)
    
    product = Product.query.filter_by(user_id=user_id, id=id).first()

    if not product:
        raise NotFoundError("product not found")

    price = PriceHistory(product_id=id, **validated_price)
    
    db.session.add(price)
    db.session.commit()
    
    return price

def view_product_prices_stats_by_id_service(user_id: int, product_id: int, fields: str):
    validated_fields = validate_price_fields(fields)

    product = Product.query.filter_by(user_id=user_id, id=product_id).first()
    if not product:
        raise NotFoundError("product not found")

    prices_query = db.session.query(PriceHistory).filter_by(product_id=product_id)
    if not prices_query.first():
        raise NotFoundError("price not found")

    stats = calculate_stats(prices_query, validated_fields)
    return stats
    
        
     
    