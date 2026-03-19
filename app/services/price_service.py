from app.models.product_model import Product
from app.models.price_history_model import PriceHistory
from app.db import db
from app.exceptions import NotFoundError
from app.validators.price_validators import validate_price_fields
from app.services.price_stats import calculate_stats
from app.validators.price_validators import validate_scraped_price
from app.services.scrapers.scraper_resolver import get_scraper

def view_product_prices_by_id_service(user_id: int, id: int):
    product = Product.query.filter_by(id=id, user_id=user_id).first()
    
    if not product:
        raise NotFoundError("product not found")
    
    prices = PriceHistory.query.filter_by(product_id=id).order_by(PriceHistory.collected_at.desc()).all()
    
    return prices

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

def refresh_product_price_by_id_service(user_id: int, id: int):
    product = Product.query.filter_by(id=id, user_id=user_id).first()
    
    if not product:
        raise NotFoundError("product not found")

    product_url = product.url
    
    scraper, _ = get_scraper(product_url)
    price, _ = scraper(product_url)
    
    price = validate_scraped_price(price)
    
    product_price = PriceHistory(product_id=product.id, price=price)
    
    db.session.add(product_price)
    db.session.commit()
    
    return product_price