from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
from os import getenv
load_dotenv()
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = 'HS256'
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode['exp'] = expire
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
