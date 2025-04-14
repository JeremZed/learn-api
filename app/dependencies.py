import jwt
import base64
import time
import random
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse

from core.config import get_settings
from core.tools import hash_password, clean_item, translate
from core.models.user import User
from core.database import database
from core.exceptions import CustomHttpException

from pymongo.collection import Collection

from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from bson import ObjectId

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


async def get_current_user(
        request: Request,
        response: Response,
        db=Depends(get_db)
        ):
    """
        Permet de retourner l'utilisateur derrière le token
    """

    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    settings = get_settings()
    need_refresh_token_access = False

    if not access_token and not refresh_token:
        raise CustomHttpException(
            flag="missing_token",
            message=translate(request, "missing_token"),
            status_code=HTTP_401_UNAUTHORIZED
        )

    try:
        # On check la validité du token d'accès
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    except jwt.ExpiredSignatureError:

        try:
            # Si le token a expiré alors on tente un rafraichissement
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

            # Besoin ici de générer un nouveau token d'accès via le token de rafraichissement
            need_refresh_token_access = True

        except jwt.PyJWTError:
            raise CustomHttpException(
                flag="invalid_refresh_token",
                message=translate(request, "invalid_refresh_token"),
                status_code=HTTP_401_UNAUTHORIZED
            )

    except jwt.PyJWTError:
        raise CustomHttpException(
            flag="invalid_token",
            message=translate(request, "invalid_token"),
            status_code=HTTP_401_UNAUTHORIZED
        )

    user_id: str = payload.get("id")

    if user_id is None:
        raise CustomHttpException(
            flag="unauthenticated",
            message=translate(request, "unauthenticated"),
            status_code=HTTP_401_UNAUTHORIZED
        )

    # Création d'un nouveau token d'accès
    if need_refresh_token_access:
        new_access_token = generate_token(
            data={"id": user_id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        response.set_cookie("access_token", new_access_token, httponly=True, max_age=1800, samesite="Strict")


    collection = db.get_collection("users")
    user =  clean_item( await collection.find_one({"_id": ObjectId(user_id)}), model=User)

    request.state.current_user = user
    return user

async def check_is_admin(request: Request):
    """
        Permet de checker si l'utilisateur en cours est un admin
    """

    current_user = getattr(request.state, "current_user", None)

    if isinstance(current_user, User) == False:
        raise CustomHttpException(
            flag="forbidden",
            message=translate(request, "forbidden"),
            status_code=HTTP_403_FORBIDDEN
        )

    if current_user.is_admin() == False:
        raise CustomHttpException(
            flag="forbidden",
            message=translate(request, "forbidden"),
            status_code=HTTP_403_FORBIDDEN
        )

    return True
