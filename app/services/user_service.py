from datetime import datetime
from app.models.user_model import User
from app.db import db
from app.validators.auth_validators import validate_register_user, validate_login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.exceptions import UnauthorizedError, ConflictError

def update_last_access(user_id: int):
    user = User.query.get(user_id)

    if user:
        user.last_access = datetime.utcnow()
        db.session.commit()

def register_user_service(data):
    validated_data = validate_register_user(data)
    
    if User.query.filter_by(email=validated_data['email']).first():
        raise ConflictError("Email already registered")

    user = User(
        name=validated_data['name'],
        email=validated_data['email'],
        password=generate_password_hash(validated_data['password'])
    )
    
    db.session.add(user)
    db.session.commit()

    return user.to_dict()

def login_user_service(data):
    validated_data = validate_login_user(data)

    user = User.query.filter_by(email=validated_data['email']).first()
    
    if not user or not check_password_hash(user.password, validated_data['password']):
        raise UnauthorizedError("email or password are incorrect")
    
    return user
