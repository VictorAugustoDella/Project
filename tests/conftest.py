from flask_jwt_extended import create_access_token
import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from app import create_app
from app.db import db
from app.models.price_history_model import PriceHistory
from app.models.product_model import Product
from app.models.user_model import User


@pytest.fixture
def app():
    test_db_url = ("sqlite:///:memory:")
    
    app = create_app(database_uri=test_db_url)
    app.config.update({
        "TESTING": True,
        "JWT_SECRET_KEY": "test-secret",
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user(app):
    with app.app_context():
        user = User(name='Victor Augusto', email='teste2fixture@gmail.com', password=generate_password_hash('Senhateste4321')) 
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        yield user, token
        
@pytest.fixture
def product(app, user):
    user_obj, _ = user
    
    with app.app_context():
        product = Product(
            product='Peanut butter',
            user_id=user_obj.id)
        
        db.session.add(product)
        db.session.commit()
        db.session.refresh(product)  # garante id carregado
        
        price = PriceHistory(
            product_id=product.id,
            price=43.50
        )
        
        db.session.add(price)
        db.session.commit()
        db.session.refresh(price)

        yield product, price
        
@pytest.fixture
def auth_header(user):
    _, token = user
    return {"Authorization": f"Bearer {token}"}


