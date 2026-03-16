from app.exceptions import ValidationError
from app.utils.field_validators import is_valid_link

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

def _validate_product_link(product_link):
    
    if not product_link:
        raise ValidationError('Product link is required')
    
    if not is_valid_link(product_link):
        raise ValidationError('Invalid link')
    
    return product_link
    

def validate_product_create(data):
    if not data:
        raise ValidationError("Missing data")
    
    product_name = _validate_product_name(data.get('product'))
    product_link = _validate_product_link(data.get('link')) 
    
    return {
        'product': product_name,
        'link': product_link
    }
    

def validate_product_edit(data):
    if not data:
        raise ValidationError("Missing data")
    
    product_name = _validate_product_name(data.get('product'))
    
    return {
        'product': product_name
    }