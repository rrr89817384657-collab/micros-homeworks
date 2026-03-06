from flask import Flask, request, jsonify
import jwt
import datetime
import hashlib

app = Flask(__name__)
SECRET_KEY = 'mysecretkey123'

# In-memory база данных пользователей
users = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/v1/user', methods=['POST'])
def register():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    
    if not login or not password:
        return jsonify({'error': 'Login and password required'}), 400
    
    if login in users:
        return jsonify({'error': 'User already exists'}), 409
    
    users[login] = {
        'login': login,
        'password': hash_password(password),
        'created_at': datetime.datetime.now().isoformat()
    }
    
    return jsonify({
        'login': login,
        'created_at': users[login]['created_at']
    }), 201

@app.route('/v1/user', methods=['GET'])
def get_user_info():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Invalid token'}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        login = payload['sub']
        
        if login not in users:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'login': login,
            'created_at': users[login]['created_at']
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/v1/token', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    
    if not login or not password:
        return jsonify({'error': 'Login and password required'}), 400
    
    if login not in users or users[login]['password'] != hash_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Создаем токен с коротким сроком действия (5 минут)
    payload = {
        'sub': login,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        'token': token
    }), 200

@app.route('/v1/token/validation', methods=['GET'])
def validate_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return '', 401
    
    token = auth_header.split(' ')[1]
    
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return '', 200
    except jwt.ExpiredSignatureError:
        return '', 401
    except jwt.InvalidTokenError:
        return '', 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
