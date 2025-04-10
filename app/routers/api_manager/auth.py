from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from dependencies import get_db

from core.tools import translate, hash_password
from core.forms.front import FormRegister
from core.models.user import UserCreate, UserOut

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