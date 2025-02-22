from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from app.dependencies import get_settings
from app.core.models import User, Credential, QueryResetPassword, ResetPassword
from app.dependencies import get_db, get_token_access, get_token_password
from app.core.tools import clean_item, hash_password, verify_password
import time
from bson import ObjectId

router = APIRouter()

@router.post("/register")
async def create_user(
    user: User,
    request: Request,
    db=Depends(get_db)
    ) -> JSONResponse:

    """
        Route pour créer un compte
    """

    collection = db.get_collection("users")

    # Vérification si l'utilisateur existe déjà par son email
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        message = request.app.translator.get(request.state.current_lang, "email_already_registered")
        raise HTTPException(status_code=400, detail=message)

    # Insertion du nouvel utilisateur
    user_dict = user.model_dump()
    user_dict['password'] = hash_password(user_dict['password'])
    result = await collection.insert_one(user_dict)

    # Création de l'url vers la fiche user
    user_id = str(result.inserted_id)
    location_url = request.app.url_path_for("user.get", user_id=user_id)

    # item = clean_item(await collection.find_one({"_id": result.inserted_id}))

    message = request.app.translator.get(request.state.current_lang, "user_created_successfully", username=user.username)

    return JSONResponse(status_code=201,
                        headers={"Location": location_url},
                        content={"message": message}
    )

@router.post("/login")
async def login(
        credentials : Credential,
        request: Request,
        db=Depends(get_db),
        settings=Depends(get_settings)
    ) -> JSONResponse:

    """
        Route pour se connecter et obtenir un token d'accès
    """

    collection = db.get_collection("users")
    existing_user = await collection.find_one({"email": credentials.email})

    if existing_user is None:
        message = request.app.translator.get(request.state.current_lang, "wrong_credential")
        raise HTTPException(status_code=400, detail=message)

    password_valid = verify_password(credentials.password, existing_user['password'])

    if not password_valid:
        message = request.app.translator.get(request.state.current_lang, "wrong_credential")
        raise HTTPException(status_code=400, detail=message)

    access_token = get_token_access(data={'username' : existing_user['username']}, settings=settings)

    message = request.app.translator.get(request.state.current_lang, "user_logged_successfully")

    return JSONResponse(
        status_code=200,
        content={"message" : message, "data" : {"token": access_token, "token_type": "bearer"}}
    )

@router.post("/query-reset-password")
async def query_reset_password(
    data : QueryResetPassword,
    request: Request,
    db=Depends(get_db)) -> JSONResponse:
    """
        Route pour réinitialiser le mot de passe
    """

    collection = db.get_collection("users")
    existing_user = await collection.find_one({"email": data.email})

    if existing_user is not None:
        token_password = get_token_password()

        update_fields = {
            "token_password": token_password,
            "token_password_dt": time.time()
        }

        await collection.update_one({"_id": ObjectId(existing_user['_id'])}, {"$set": update_fields})

    message = request.app.translator.get(request.state.current_lang, "query_reset_password_successfully", email=data.email)

    return JSONResponse(status_code=200, content={"message" : message})

@router.post("/reset-password")
async def reset_password(
    data : ResetPassword,
        request: Request,
        db=Depends(get_db),
        settings=Depends(get_settings)
    ) -> JSONResponse:

    collection = db.get_collection("users")
    existing_user = await collection.find_one({"email": data.email, 'token_password' : data.token})

    # Check de l'existence de la demande de réinitialisation de mot de passe
    if existing_user is None:
        message = request.app.translator.get(request.state.current_lang, "query_reset_password_not_found")
        raise HTTPException(status_code=400, detail=message)

    duration_in_seconds = time.time() - existing_user['token_password_dt']

    # Convertion de la durée en seconde vers une durée en heure
    delta = divmod(duration_in_seconds, 3600)[0]
    if delta > settings.PASSWORD_TOKEN_EXPIRE_HOUR:
        message = request.app.translator.get(request.state.current_lang, "query_reset_password_expired")
        raise HTTPException(status_code=400, detail=message)

    # Modification du mot de passe
    update_fields = {
        "password": hash_password(data.password),
        "token_password" : None,
        "token_password_dt": None
    }

    await collection.update_one({"_id": ObjectId(existing_user['_id'])}, {"$set": update_fields})

    message = request.app.translator.get(request.state.current_lang, "reset_password_successfully", email=data.email)

    return JSONResponse(status_code=200, content={"message" : message})