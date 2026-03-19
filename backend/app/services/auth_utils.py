import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from pwdlib import PasswordHash

# Configuration using your existing environment variables
# We'll use your LLM key as a seed for the secret if nothing else is set
SECRET_KEY = os.getenv("LLM_API_KEY", "trading_secret_key_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # 24 Hours

# Initialize Argon2 password hashing
password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    """Hashes a plain text password for secure storage."""
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if the provided password matches the stored hash."""
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generates a secure JWT for the user session."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
