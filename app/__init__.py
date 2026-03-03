from flask import Flask, jsonify
from app.db import db
from app.routes.auth import auth_bp
from app.routes.product import product_bp
from app.routes.price import price_bp
from os import getenv
from flask_jwt_extended import JWTManager, get_jwt_identity
from app.models.user_model import User
from app.models.product_model import Product
from app.models.price_history_model import PriceHistory
from app.exceptions import ValidationError, NotFoundError, ConflictError, ValueError
from flask_jwt_extended import verify_jwt_in_request
from app.services.user_service import update_last_access


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = getenv('SECRET_KEY', 'dev-secret-key')
    
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    JWTManager(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    
    db.init_app(app)
    
    app.register_blueprint(product_bp, url_prefix='/api/v1/product')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(price_bp, url_prefix='/api/v1/price')
    
    # Handlers de erro

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"error": str(e)}),400
    
    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return jsonify({"error": str(e)}), 401
    
    @app.errorhandler(NotFoundError)
    def handle_not_found_error(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(ConflictError)
    def handle_conflict_error(e):
        return jsonify({"error": str(e)}), 409
    
    
    # update last access
    @app.before_request
    def update_user_activity():
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            
            if user_id:
                update_last_access(user_id)
        except Exception:
            pass
   
    with app.app_context():
        db.create_all()

    return app