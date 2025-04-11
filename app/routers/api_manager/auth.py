from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_200_OK, HTTP_201_CREATED

from dependencies import get_db, get_settings, get_token_access, get_current_user, get_token_password

from core.tools import translate, verify_password, clean_item, hash_password
from core.forms.front import FormRegister, FormLogin,FormQueryResetPassword, FormResetPassword
from core.models.user import UserCreate, User, UserOut

from repo.user import UserRepository
import time

router = APIRouter(prefix=f"/auth", tags=["auth"])

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
    existing_user = await repo.check_exists({"email": form.email})

    if existing_user:

        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "flag": "form_value_error",
                "message" : translate(request, "email_already_registered"),
                "data": [ { "field" : "email", "msg" : translate(request, "email_already_registered")}]
            } )

    # Insertion du nouvel utilisateur
    new_user = UserCreate(**form.model_dump())
    user_dict = new_user.model_dump(exclude={"id"})

    result = await repo.create(user_dict)

    message = translate(request, "user_created_successfully", username=new_user.username)

    return JSONResponse(status_code=HTTP_201_CREATED, content={
        "message": message
    })

@router.post("/login", name="auth.login")
async def login(
    request: Request,
    form : FormLogin,
    db=Depends(get_db),
    settings=Depends(get_settings)
    ) -> JSONResponse:

    """
        Route pour l'identification de l'utilisateur
    """

    repo = UserRepository(db)
    existing_user = clean_item( await repo.check_email_exists(form.email), model=User)

    if existing_user is None:

        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "flag": "wrong_credential",
                "message" : translate(request, "wrong_credential"),
                "data": [ ]
            } )

    password_valid = verify_password(form.password, existing_user.password)

    if not password_valid:
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "flag": "wrong_credential",
                "message" : translate(request, "wrong_credential"),
                "data": [ ]
            } )

    access_token = get_token_access(data={'id' : existing_user.id }, settings=settings)

    message = translate(request, "user_logged_successfully")

    response = JSONResponse(
        status_code=200,
        content={
            "message" : message,
            "data" : {
                "user" : UserOut(**existing_user.model_dump()).model_dump()
            }
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="Strict",
        max_age=3600,
        path="/"
    )
    return response

@router.get("/me", name="auth.me")
async def who_me(
        request: Request,
        user= Depends(get_current_user),
    ) -> JSONResponse:

    """
        Route qui permet de retourner les informations de l'utilisateur actuellement connecté via son token
    """

    return JSONResponse(status_code=HTTP_200_OK, content={
        "message" : "OK",
        "data" : {
            "user" : UserOut(**user.model_dump()).model_dump()
        }
    })

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
    existing_user = clean_item(await repo.check_email_exists(form.email), model=User)

    if not existing_user:
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "flag": "wrong_credential",
                "message" : translate(request, "wrong_credential"),
                "data": [ ]
            } )

    token_password = get_token_password()

    update_fields = {
        "token_password": token_password,
        "token_password_dt": time.time()
    }

    await repo.update(id=existing_user.id, update_data=update_fields )

    return JSONResponse(status_code=HTTP_200_OK, content={
        "message" : translate(request, "query_reset_password_successfully", email=existing_user.email)
    })

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
    existing_user = clean_item(await repo.check_token_reset_password(form.email, form.token), model=User)

    # Check de l'existence de la demande de réinitialisation de mot de passe
    if existing_user is None:
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content=
            {
                "flag": "query_reset_password_not_found",
                "message" : translate(request, "query_reset_password_not_found"),
                "data": [ ]
            })

    duration_in_seconds = time.time() - existing_user.token_password_dt

    # Convertion de la durée en seconde vers une durée en heure
    delta = divmod(duration_in_seconds, 3600)[0]
    if delta > settings.PASSWORD_TOKEN_EXPIRE_HOUR:
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content=
            {
                "flag": "query_reset_password_expired",
                "message" : translate(request, "query_reset_password_expired"),
                "data": [ ]
            })

    # Modification du mot de passe
    update_fields = {
        "password": hash_password(form.password),
        "token_password" : None,
        "token_password_dt": None
    }
    await repo.update(id=existing_user.id, update_data=update_fields )

    return JSONResponse(status_code=HTTP_200_OK, content={
        "message" : translate(request, "reset_password_successfully", email=existing_user.email)
    })
