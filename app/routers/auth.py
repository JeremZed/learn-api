from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import create_access_token, Token, get_settings, verify_token
from app.core.models import User
from app.dependencies import get_db
from app.core.tools import clean_item, hash_password, verify_password
# from app.core.translation import translation_manager

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    settings=Depends(get_settings)
    ):
    # Tu devrais ici vérifier les informations d'identification de l'utilisateur
    # Par exemple, tu peux vérifier un mot de passe dans une base de données
    if form_data.username == "jessica" and form_data.password == "password":  # A améliorer !

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/refresh")
async def refresh_access_token(
    refresh_token: str,
    settings=Depends(get_settings)
    ):

    payload = verify_token(refresh_token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Vérifie si le refresh token est valide (par exemple, s'il est dans la base de données)
    # et non révoqué.
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def create_user(
    user: User,
    request: Request,
    db=Depends(get_db)
    ) -> JSONResponse:

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

    return JSONResponse(status_code=201,
                        headers={"Location": location_url},
                        content={"message": "User created successfully"}
    )
