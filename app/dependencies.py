import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Security, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.core.config import get_settings

from pymongo.collection import Collection
from app.core.database import database


def get_db() -> Collection:
    return database.db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

def create_access_token(data: dict,
        expires_delta: Optional[timedelta] = None
    ):
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        settings = get_settings()
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = verify_token(token)
    username: str = payload.get("sub")
    print(username)
    if username is None:
        raise HTTPException(status_code=401, detail="Token is invalid")
    return User(username=username)


