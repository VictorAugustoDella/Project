from app.exceptions import ValidationError, ConflictError
from app.utils.validators import is_valid_email, is_valid_full_name, is_valid_password
from app.models.user_model import User

def validate_register_user(data):
    user_name = data.get('name')
    user_email = data.get('email')
    user_password = data.get('password')

    if not (user_password and user_email and user_name):
        raise ValidationError('Name, email and password are required')
    
    if not is_valid_full_name(user_name):
        raise ValidationError('Invalid name')
    
    if not is_valid_email(user_email):
        raise ValidationError('Invalid e-mail')
    
    if not is_valid_password(user_password):
        raise ValidationError('Weak password [min 8 characters, 1 uppercase, 1 lowercase and 1 number ]')
    
    if User.query.filter_by(email=user_email).first():
        raise ConflictError("Email already registered")
    
    user_email = user_email.strip().lower()
    user_name = user_name.strip().title()
    
    return {
        'name': user_name,
        'email': user_email,
        'password': user_password
    }
    
def validate_login_user(data):
    if not data:
        raise ValidationError("missing data")
    
    email = data.get('email')
    password = data.get('password')

    if not (password and email):
        raise ValidationError("email and password are required")
    
    return {
        "email": email.strip().lower(),
        "password": password
    }
    