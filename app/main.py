from fastapi import FastAPI
from contextlib import asynccontextmanager

import app.routers as routes
import app.routers.auth as router_auth
from app.core.database import database
from app.core.translation import TranslationManager
from app.middleware import TranslateMiddleware



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
app.add_middleware(TranslateMiddleware)

app.include_router(routes.users.router)
app.include_router(router_auth.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}