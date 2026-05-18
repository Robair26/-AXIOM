import os
import hashlib
import hmac
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv("SECRET_KEY", "axiom-secret-key-change-in-production")

def generate_token(user_id="robair"):
    """Generate a JWT token for authentication"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    """Verify a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to protect API endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "No token provided"}), 401
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        return f(*args, **kwargs)
    return decorated

def hash_api_key(api_key):
    """Hash an API key for secure storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()

def rate_limit_check(ip, requests_store, max_requests=60):
    """Simple rate limiting — max 60 requests per minute"""
    now = datetime.utcnow()
    minute_ago = now - timedelta(minutes=1)
    
    if ip not in requests_store:
        requests_store[ip] = []
    
    requests_store[ip] = [t for t in requests_store[ip] if t > minute_ago]
    
    if len(requests_store[ip]) >= max_requests:
        return False
    
    requests_store[ip].append(now)
    return True
