from flask import request, jsonify
from app.routes.product import product_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.product_service import view_products_service, view_product_by_id_service, create_product_service, edit_product_service, delete_product_service

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def view_products():
    user_id = int(get_jwt_identity())

    products = view_products_service(user_id)
    
    return jsonify([p.to_dict() for p in products]), 200

@product_bp.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def view_product_by_id(id):
    user_id = int(get_jwt_identity())

    product = view_product_by_id_service(id, user_id)
    
    return jsonify(product.to_dict()), 200

@product_bp.route('/products', methods=['POST']) 
@jwt_required()
def create_product():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    new_product = create_product_service(user_id, data)
    
    return jsonify(new_product.to_dict()), 201

@product_bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def edit_product(id):
    user_id = int(get_jwt_identity())   
    data = request.get_json()
    
    product = edit_product_service(user_id, id, data)

    return jsonify(product.to_dict()), 200

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    user_id = int(get_jwt_identity())
    
    delete_product_service(user_id, id)

    return '', 204
      