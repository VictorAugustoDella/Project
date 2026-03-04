def test_register_sucess(client):
    response = client.post(
        '/api/v1/auth/register', 
        json={
            "name": "Teste Fixture", 
            "email": "testefixture@gmail.com", 
            "password":"Senhateste4321"
            }
        )
    
    data = response.get_json()
    
    assert response.status_code == 201
    assert {'id', 'email'}.issubset(data)
    assert 'password' not in data
    
def test_register_duplicate_email(client, user):
    response = client.post(
        '/api/v1/auth/register', 
        json={
            "name": "Teste Fixture", 
            "email": "teste2fixture@gmail.com",
            "password":"Senhateste4321"
            }
        )
    
    data = response.get_json()
    
    assert response.status_code == 409
    assert "Email already registered" in data['error']
    
def test_register_missing_field(client):
    response = client.post(
        '/api/v1/auth/register',
        json={
            "name": "Teste Fixture", 
            "email": "testefixture@gmail.com"
            }
        )
    
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'Name, email and password are required' in data['error']

def test_register_invalid_email(client):
    response = client.post(
        '/api/v1/auth/register',
        json={
            "name": "Teste Fixture", 
            "email": "gmail.com", 
            "password": "Senhateste4321"
            }
        )
    
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'Invalid e-mail' in data['error']

def test_register_weak_password(client):
    response = client.post(
        '/api/v1/auth/register',
        json={
            "name": "Teste Fixture",
            "email": "testefixture@gmail.com",
            "password": "weakpassword"
            }
        )
    
    data = response.get_json()
    
    assert response.status_code == 400
    assert 'Weak password [min 8 characters, 1 uppercase, 1 lowercase and 1 number]' in data['error']
    
    
    
    
def test_login_success(client, user):
    response = client.post(
        '/api/v1/auth/login', 
        json={
            "email": "teste2fixture@gmail.com", 
            "password": "Senhateste4321"
            }
        )
    
    data = response.get_json()
    
    assert response.status_code == 200
    assert "access_token" in data

def test_login_wrong_password(client, user):
    response = client.post(
        '/api/v1/auth/login', 
        json={
            "email": "teste2fixture@gmail.com", 
            "password": "wrongpassword"
            }
        )
    
    data = response.get_json()
    
    assert response.status_code == 401
    assert "email or password are incorrect" in data['error']
    
def test_login_user_not_found(client, user):
    response = client.post(
        '/api/v1/auth/login', 
        json={
            "email": "inexistentfixture@gmail.com", 
            "password": "Senhateste4321"
            }
        )
    
    data = response.get_json()
    
    assert response.status_code == 401
    assert "email or password are incorrect" in data['error']

def test_login_missing_field(client, user):
    response = client.post(
        '/api/v1/auth/login', 
        json={
            "email": "teste2fixture@gmail.com@gmail.com"
            }
        )
    
    data = response.get_json()
    
    assert response.status_code == 400
    assert "email and password are required" in data['error']