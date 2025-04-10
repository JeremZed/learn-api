from fastapi import FastAPI
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from contextlib import asynccontextmanager

import routers.api_manager.auth as route_manager
from core.database import database
from core.translation import TranslationManager
from core.exceptions import validation_exception_handler, model_validation_exception_handler
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

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, model_validation_exception_handler)

# Autoriser le frontend Vue.js à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TranslateMiddleware)

app.include_router(route_manager.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}