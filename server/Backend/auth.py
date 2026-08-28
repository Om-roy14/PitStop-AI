import os
from datetime import datetime, timedelta

import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from Backend.Databases.database import get_db
from Backend.Databases.models import User

# =========================================
# SECURITY CONFIGURATION
# =========================================
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "pitstop-production-secure-key-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 Days

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# =========================================
# PASSWORD & TOKEN UTILITIES
# =========================================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    # bcrypt limits passwords to 72 bytes
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
        
    return user

# =========================================
# REGISTRATION LOGIC
# =========================================
def register_user(db: Session, name: str, email: str, password: str, linkedin_id: str, github_id: str):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None

    new_user = User(
        name=name,
        email=email,
        password=get_password_hash(password), 
        linkedin_id=linkedin_id,
        github_id=github_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# =========================================
# LOGIN LOGIC
# =========================================
def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user