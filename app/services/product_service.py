from app.models.product_model import Product
from app.models.price_history_model import PriceHistory
from app.db import db
from app.validators.product_validators import validate_product_create, validate_product_edit
from app.exceptions import NotFoundError, ConflictError
from app.validators.price_validators import validate_scraped_price
from app.services.scrapers.scraper_resolver import get_scraper

def view_products_service(user_id: int):
    products = Product.query.filter_by(user_id=user_id).all()
    
    return products
    
def view_product_by_id_service(product_id: int, user_id: int):
    product = Product.query.filter_by(id=product_id, user_id=user_id).first()
    
    if not product:
        raise NotFoundError("product not found")
    
    return product

def create_product_service(user_id: int, data):
    validated_product = validate_product_create(data)
    
    product_url = validated_product['url']
    
    existing_product = Product.query.filter_by(user_id=user_id, url=product_url).first()

    if existing_product:
        raise ConflictError("you already registered this product link")
    
    scraper, site = get_scraper(product_url)
    price, scraped_name = scraper(product_url)  
        
    price = validate_scraped_price(price)
        
    new_product = Product(user_id=user_id, **validated_product, site=site, scraped_name=scraped_name)
    
    db.session.add(new_product)
    db.session.flush() # gera o ID ainda sem o commit
    
    product_price = PriceHistory(product_id=new_product.id, price=price)

    db.session.add(product_price)
    db.session.commit()
    
    return new_product

def edit_product_service(user_id: int, product_id: int, data ):
    validated_product = validate_product_edit(data)
    
    product = Product.query.filter_by(id=product_id, user_id=user_id).first()
    
    if not product:
        raise NotFoundError("product not found")
    
    product.product = validated_product['product']
    
    db.session.commit()
    
    return product

def delete_product_service(user_id: int, product_id: int):
    product = Product.query.filter_by(id=product_id, user_id=user_id).first()
    
    if not product:
        raise NotFoundError("product not found")
    
    db.session.delete(product)
    db.session.commit()
    
    #Sem necessidade de retorno nesse service, apenas executa uma ação