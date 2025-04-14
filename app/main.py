from fastapi import FastAPI, Request
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager

import routers.api_manager.auth as route_auth
import routers.api_manager.account as route_account

from core.database import database
from core.translation import TranslationManager
from core.exceptions import validation_exception_handler, model_validation_exception_handler, CustomHttpException
from middleware import TranslateMiddleware


@asynccontextmanager
async def lifespan(app):
    await database.connect()

    # Initialisation de la gestion des trads
    translation_manager = TranslationManager()
    translation_manager.load_translations()

    app.translator = translation_manager

    yield

    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(CustomHttpException)
async def custom_http_exception_handler(request: Request, exc: CustomHttpException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "flag": exc.flag,
            "message": exc.message,
            "data": exc.data
        }
    )

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, model_validation_exception_handler)

# Autoriser le frontend Vue.js à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TranslateMiddleware)
# app.add_middleware(AuthMiddleware)

app.include_router(route_auth.router)
app.include_router(route_account.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}