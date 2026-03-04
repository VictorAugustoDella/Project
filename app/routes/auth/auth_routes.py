from flask import request, jsonify
from app.routes.auth import auth_bp
from flask_jwt_extended import create_access_token
from app.services.user_service import register_user_service, login_user_service

@auth_bp.route('/register', methods=['POST'])
def register_user():   
    data = request.get_json()
    
    user=register_user_service(data)
    
    return jsonify(user), 201

@auth_bp.route('/login', methods=['POST'])
def login_user():   
    data = request.get_json()

    user = login_user_service(data)
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify(access_token=access_token), 200
    