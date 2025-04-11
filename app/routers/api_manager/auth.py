from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from dependencies import get_db, get_settings, get_token_access, get_current_user

from core.tools import translate, verify_password, clean_item
from core.forms.front import FormRegister, FormLogin
from core.models.user import UserCreate, User, UserOut

from repo.user import UserRepository

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

    return JSONResponse(status_code=201, content={
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

    return JSONResponse(status_code=200, content={
        "message" : "OK",
        "data" : {
            "user" : UserOut(**user.model_dump()).model_dump()
        }
    })