import bcrypt
import jwt
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'change_me')

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict, expires_delta: int = None) -> str:
    to_encode = data.copy()
    expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '1440')) if expires_delta is None else expires_delta
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expire_minutes)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm='HS256')
    return encoded_jwt

def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
