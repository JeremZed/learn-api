from fastapi import APIRouter, Request, Depends, HTTPException
from core.forms.front import FormChangePassword
from core.tools import translate, hash_password, verify_password
from core.models.user import check_valid_password
from dependencies import get_db, get_current_user
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_422_UNPROCESSABLE_ENTITY
from core.exceptions import CustomHttpException
from repo.user import UserRepository

router = APIRouter(prefix=f"/account", tags=["account"])


@router.put("/password", name="account.change_password")
async def change_password(
    request: Request,
    form: FormChangePassword,
    user= Depends(get_current_user),
    db=Depends(get_db)
    ) -> JSONResponse:

    """
        Route pour modifier le mot de passe du compte
    """

    # On check que le nouveau mot de passe soit conforme
    try:
        new_password = check_valid_password(form.new_password)
    except Exception as e:
        raise CustomHttpException(
            flag="form_value_error",
            message=translate(request, "password_not_valid"),
            status_code=HTTP_401_UNAUTHORIZED,
            data=[{ "field" : "new_password", "msg" : translate(request, "password_not_valid")}]
        )

    # On check l'identification du mot de passe
    password_valid = verify_password(form.current_password, user.password)

    if not password_valid:
        raise CustomHttpException(
            flag="form_value_error",
            message=translate(request, "wrong_credential"),
            status_code=HTTP_401_UNAUTHORIZED,
            data=[{ "field" : "current_password", "msg" : translate(request, "wrong_credential")}]
        )

    # On s'assure que le nouveau mot de passe ne correspond pas au mot de passe actuel
    password_no_change = verify_password(form.new_password, user.password)

    if password_no_change:
        raise CustomHttpException(
            flag="form_value_error",
            message=translate(request, "password_need_change"),
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            data=[{ "field" : "new_password", "msg" : translate(request, "password_need_change")}]
        )

    # Modification du mot de passe de l'utilisateur

    user.password = new_password

    user_dict = user.model_dump(exclude={"id"})
    repo = UserRepository(db)
    result = await repo.update(id=user.id, update_data=user_dict)

    message = translate(request, "account_updated_successfully")

    return JSONResponse(status_code=HTTP_200_OK, content={
        "message": message
    })