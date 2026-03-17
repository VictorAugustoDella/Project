from app.exceptions import ValidationError
from app.utils.field_validators import is_valid_url

def _validate_product_name(product_name):
    
    if not product_name:
        raise ValidationError('Product is required')
    
    # Verificando se é uma string
    if not isinstance(product_name, str):
        raise ValidationError('Product must be a string')
    
    product_name = product_name.strip()
    
    if len(product_name) == 0:
        raise ValidationError('Product cannot be empty')
    
    return product_name

def _validate_product_url(product_url):
    
    if not product_url:
        raise ValidationError('Product url is required')
    
    if not is_valid_url(product_url):
        raise ValidationError('Invalid url')
    
    return product_url
    

def validate_product_create(data):
    if not data:
        raise ValidationError("Missing data")
    
    product_name = _validate_product_name(data.get('product'))
    product_url = _validate_product_url(data.get('url')) 
    
    return {
        'product': product_name,
        'url': product_url
    }
    

def validate_product_edit(data):
    if not data:
        raise ValidationError("Missing data")
    
    product_name = _validate_product_name(data.get('product'))
    
    return {
        'product': product_name
    }