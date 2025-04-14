from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST

def get_msg_errors_validation(exc: ValidationError) -> list:
    """
        Permet de retourner une liste des messages d'erreur retournés par la classe ValidationError de pydantic
    """
    errors = []
    for e in exc.errors():
        print(e)
        errors.append({
            "field": e['loc'][0],
            "msg": str(e['ctx'].get('error', 'Erreur de validation inconnue'))
        })
    return errors

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = get_msg_errors_validation(exc)
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "flag": "form_value_error",
            "data": errors
        }
    )

async def model_validation_exception_handler(request: Request, exc: ValidationError):
    errors = get_msg_errors_validation(exc)
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "flag": "form_value_error",
            "data": errors
        }
    )

class CustomHttpException(Exception):
    def __init__(self, flag: str, message: str, status_code: int = HTTP_400_BAD_REQUEST, data=None):
        self.flag = flag
        self.message = message
        self.status_code = status_code
        self.data = data or []
