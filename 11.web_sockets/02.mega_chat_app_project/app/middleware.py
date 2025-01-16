import jwt
from functools import wraps
from flask import request, jsonify
from config import JWT_KEY

# JWT authentication middleware
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('hart')
        print("token")
        print(token)
        if not token:
            return jsonify({'message': 'unauthorized'}), 401

        try:
            payload = jwt.decode(token, JWT_KEY, algorithms=["HS256"])
            request.current_user = payload  # Attach the payload to request
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'invalid token'}), 401

        return f(*args, **kwargs)
    return decorated_function
