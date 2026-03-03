from app.exceptions import ValidationError

def _validate_product_name(product_name):
    
    if not product_name:
        raise ValidationError('Product is required')
    
    # Verificando se é uma string
    if not isinstance(product_name, str):
        raise ValidationError('Product must be a string')
    
    product_name = product_name.strip()
    
    if len(product_name) == 0:
        raise ValidationError('Product cannot be empty')
    
    return product_name.capitalize()
    

def validate_product_create(data):
    if not data:
        raise ValidationError("Missing data")
    
    product_name = _validate_product_name(data.get('product'))
    
    return {
        'product': product_name.capitalize()
    }
    

def validate_product_edit(data):
    if not data:
        raise ValidationError("Missing data")
    
    product_name = _validate_product_name(data.get('product'))
    
    return {
        'product': product_name.capitalize()
    }