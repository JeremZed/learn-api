import jwt
import base64
import time
import random
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Security, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from core.config import get_settings
from core.tools import hash_password
from core.models import UserCurrent, ROLE_NONE, ROLE_ADMIN
from pymongo.collection import Collection
from core.database import database
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
        data=data, expires_delta=access_token_expires
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
        Permet de vérifier la validité du token et de retourner celui-ci si pas de soucis
    """
    try:
        settings = get_settings()
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(
        request: Request,
        token: str = Security(oauth2_scheme),
        db=Depends(get_db)
        ):
    """
        Permet de retourner l'utilisateur derrière le token
    """

    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication token")

    payload = verify_token(token)
    user_id: str = payload.get("id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Token is invalid")

    collection = db.get_collection("users")
    existing_user = await collection.find_one({"_id": ObjectId(user_id)})

    user = UserCurrent(
        username=existing_user['username'],
        email=existing_user['email'],
        name=existing_user['name'],
        role=existing_user.get('role', ROLE_NONE),
    )

    request.state.current_user = user
    return user

async def check_is_admin(request: Request):
    """
        Permet de checker si l'utilisateur en cours est un admin
    """

    current_user = getattr(request.state, "current_user", None)

    if isinstance(current_user, UserCurrent) == False:
        raise HTTPException(status_code=403, detail="Forbidden")

    if current_user.is_admin() == False:
        raise HTTPException(status_code=403, detail="Forbidden")

    return True
