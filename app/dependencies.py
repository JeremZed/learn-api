import jwt
import base64
import time
import random
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException
from app.core.config import get_settings
from app.core.tools import hash_password

from pymongo.collection import Collection
from app.core.database import database


def get_db() -> Collection:
    """
        Permet de retourner la session de connexion à la base de donnée
    """
    return database.db

def get_token_access(data:dict, settings:dict) -> dict:
    """
        Permet de retourner un token
    """

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(
        data={ "username": data['username'] }, expires_delta=access_token_expires
    )

    return access_token

def get_token_password() -> dict:
    """
        Permet de retourner un token de réinitialisation de mot de passe
    """
    t = str(time.time)
    i = random.randint(0, 9999)

    token = hash_password(f"{t}-{i}")
    return base64.b64encode(token.encode("ascii")).decode('utf-8')

def generate_token(data: dict, expires_delta: Optional[timedelta] = None ) -> str:
    """
        Permet de créer un token d'accès
    """
    settings = get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """
        Permet de vérifier la validité du token
    """
    try:
        settings = get_settings()
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



def get_current_user(token: str) -> dict:
    """
        Permet de retourner l'utilisateur derrière le token
    """
    payload = verify_token(token)

    username: str = payload.get("sub")

    print(username)
    if username is None:
        raise HTTPException(status_code=401, detail="Token is invalid")
    # return
    return {"todoo" : "retourner l'utilisateur en cours..."}


