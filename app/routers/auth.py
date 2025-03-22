from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from dependencies import get_settings
from core.models import User, ROLE_USER
from core.forms.front import FormRegister, FormLogin, FormQueryResetPassword, FormResetPassword
from dependencies import get_db, get_token_access, get_token_password
from core.tools import clean_item, hash_password, verify_password, get_message
import time
from bson import ObjectId

from repo.user import UserRepository
from routers.base_router import create_crud_routes

router = APIRouter(prefix=f"/auth", tags=["auth"])

@router.post("/login", name="auth.login")
async def login(
    request: Request,
    form : FormLogin,
    db=Depends(get_db),
    settings=Depends(get_settings)
    ):

    repo = UserRepository(db)
    existing_user =  clean_item(await repo.check_email_exists(form.email), model=User)

    if existing_user is None:
        message = get_message(request, "wrong_credential")
        raise HTTPException(status_code=400, detail={
            "flag" : "wrong_credential",
            "message" : message
            })

    password_valid = verify_password(form.password, existing_user.password)

    if not password_valid:
        message = get_message(request, "wrong_credential")
        raise HTTPException(status_code=400, detail={"message" : message})

    access_token = get_token_access(data={'id' : existing_user.id }, settings=settings)

    message = get_message(request, "user_logged_successfully")

    return JSONResponse(
        status_code=200,
        content={"message" : message, "data" : {"token": access_token, "token_type": "Bearer"}}
    )

@router.post("/register", name="auth.register")
async def create_user(
    request: Request,
    form: FormRegister,
    db=Depends(get_db)
    ) -> JSONResponse:

    """
        Route pour créer un compte
    """

    repo = UserRepository(db)

    # Vérification si l'utilisateur existe déjà par son email
    existing_user = await repo.check_email_exists(form.email)

    if existing_user:
        message = get_message(request, "email_already_registered")
        raise HTTPException(status_code=400, detail=message)

    # Insertion du nouvel utilisateur
    new_user = User(
        username=form.username,
        name=form.name,
        email=form.email,
        role= ROLE_USER,
        password=hash_password(form.password)
    )

    result = await repo.create(new_user.model_dump(exclude=['id']))

    message = get_message(request, "user_created_successfully", username=new_user.username)

    return JSONResponse(status_code=201, content={"message": message})


@router.post("/query-reset-password", name="auth.query_reset_password")
async def query_reset_password(
    form : FormQueryResetPassword,
    request: Request,
    db=Depends(get_db)) -> JSONResponse:
    """
        Route pour faire une demande de réinitialisation le mot de passe
    """

    repo = UserRepository(db)

    # Vérification si l'utilisateur existe déjà par son email
    existing_user = clean_item(await repo.check_email_exists(form.email), model=User, exclude=['password'])

    if not existing_user:
        message = get_message(request, "users_not_found")
        raise HTTPException( status_code=404, detail=message )

    token_password = get_token_password()

    update_fields = {
        "token_password": token_password,
        "token_password_dt": time.time()
    }

    await repo.update(id=existing_user.id, update_data=update_fields )

    message = get_message(request, "query_reset_password_successfully", email=existing_user.email)

    return JSONResponse(status_code=200, content={"message" : message})

@router.post("/reset-password", name="auth.reset_password")
async def reset_password(
        form : FormResetPassword,
        request: Request,
        db=Depends(get_db),
        settings=Depends(get_settings)
    ) -> JSONResponse:

    """
        Route pour réinitialiser le mot de passe
    """

    repo = UserRepository(db)

    # Vérification si l'utilisateur existe déjà par son email
    existing_user = clean_item(await repo.check_token_reset_password(form.email, form.token), model=User, exclude=['password'])

    # Check de l'existence de la demande de réinitialisation de mot de passe
    if existing_user is None:
        message = get_message(request, "query_reset_password_not_found")
        raise HTTPException(status_code=400, detail=message)

    duration_in_seconds = time.time() - existing_user.token_password_dt

    # Convertion de la durée en seconde vers une durée en heure
    delta = divmod(duration_in_seconds, 3600)[0]
    if delta > settings.PASSWORD_TOKEN_EXPIRE_HOUR:
        message = get_message(request, "query_reset_password_expired")
        raise HTTPException(status_code=400, detail=message)

    # Modification du mot de passe
    update_fields = {
        "password": hash_password(form.password),
        "token_password" : None,
        "token_password_dt": None
    }
    await repo.update(id=existing_user.id, update_data=update_fields )

    message = get_message(request, "reset_password_successfully", email=form.email)

    return JSONResponse(status_code=200, content={"message" : message})