import os
import re
import bcrypt
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt_identity


# Load secrets
load_dotenv()
MONGO_URL = os.getenv('MONGO_URL')
JWT_SECRET = os.getenv('JWT_SECRET')
if not MONGO_URL or not JWT_SECRET:
    raise ValueError('Mongo URL or JWT secret not found.')


# MongoDB connection
def connect_mongodb():
    client = MongoClient(MONGO_URL, retryWrites=False)
    db = client['DevBot']
    return db['users']


# Email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# Register user
def register_user(name, email, password):
    try:
        if not all([name, email, password]):
            return {'error': 'All fields are required'}, 400
        
        if not is_valid_email(email):
            return {'error': 'Invalid email format'}, 400
        
        if len(password) < 8:
            return {'error': 'Password must be at least 8 characters'}, 400

        users = connect_mongodb()
        if users.find_one({'email': email}):
            return {'error': 'User already exists!'}, 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user = {
            'name': name.strip(),
            'email': email.lower(),
            'password': hashed_password,
            'created_at': datetime.now(timezone.utc)
        }
        result = users.insert_one(user)
        
        if not result.acknowledged:
            return {'error': 'Failed to create user!'}, 500
        
        return {
            'message': 'User registered successfully',
            'user_id': str(result.inserted_id)
        }, 201
    
    except Exception as e:
        return {'error': f'Failed to create user! {str(e)}'}, 500


# Login user
def login_user(email, password):
    try:
        if not all([email, password]):
            return {'error': 'Email and password are required'}, 400
            
        users = connect_mongodb()
        user = users.find_one({'email': email.lower()})
        
        if not user:
            return {'error': 'Invalid credentials!'}, 401
        
        if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return {'error': 'Invalid credentials!'}, 401
        
        additional_claims = {
            'name': user['name'],
            'email': user['email']
        }
        access_token = create_access_token(
            identity=str(user['_id']),
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=1)
        )
        
        return {
            'message': 'Login successful',
            'access_token': access_token,
        }, 200
    
    except Exception as e:
        return {'error': f'Failed to login user! {str(e)}'}, 500


# Get current user 
def get_current_user():
    user_id = get_jwt_identity()
    users = connect_mongodb()
    user = users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return {'error': 'User not found'}, 404
    return {
        'id': str(user['_id']),
        'name': user['name'],
        'email': user['email']
    }, 200
