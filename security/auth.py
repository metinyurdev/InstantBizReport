from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Optional
from .hash import verify_password
from models.tables import users_table
from models.database import get_db
from pydantic import BaseModel

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Kara liste için basit bir set
blacklisted_tokens = set()


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def authenticate_user(db: Session, username: str, password: str):
    user = db.execute(users_table.select().where(users_table.c.username == username)).fetchone()
    if not user:
        return False
    user_dict = dict(user._mapping)
    if not verify_password(password, user_dict['password']):
        return False
    return user_dict

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        # Token'ın kara listede olup olmadığını kontrol et
        if token in blacklisted_tokens:
            raise credentials_exception
        
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.execute(users_table.select().where(users_table.c.username == token_data.username)).fetchone()
    if user is None:
        raise credentials_exception
    return dict(user._mapping)

def logout(token: str = Depends(oauth2_scheme)):
    # Token'ı kara listeye ekle
    blacklisted_tokens.add(token)
    return {"message": "Successfully logged out"}