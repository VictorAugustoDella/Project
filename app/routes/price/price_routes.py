from flask import request, jsonify
from app.routes.price import price_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.price_service import view_product_prices_by_id_service, add_product_prices_by_id_service, view_product_prices_stats_by_id_service

@price_bp.route('/products/<int:id>/prices', methods=['GET'])
@jwt_required()
def view_product_prices_by_id(id):
    user_id = int(get_jwt_identity())

    prices = view_product_prices_by_id_service(user_id, id)
    
    return jsonify([p.to_dict() for p in prices]), 200

@price_bp.route('/products/<int:id>/prices', methods=['POST'])
@jwt_required()
def add_product_prices_by_id(id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    price = add_product_prices_by_id_service(user_id, id, data)
    
    return jsonify(price.to_dict()), 201

@price_bp.route('/products/<int:id>/prices/stats', methods=['GET'])
@jwt_required()
def view_product_prices_stats_by_id(id):
    user_id = int(get_jwt_identity())
    fields = request.args.get('fields')
    
    stats = view_product_prices_stats_by_id_service(user_id, id, fields)
    
    return jsonify(stats)