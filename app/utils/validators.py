import re

def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_full_name(name: str) -> bool:
    pattern = r"^[A-Za-zÀ-ÿ]+([ '-][A-Za-zÀ-ÿ]+)*$"
    return bool(re.match(pattern, name.strip())) and len(name.split()) >= 2

def is_valid_password(password: str) -> bool:
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    return re.match(pattern, password) is not None