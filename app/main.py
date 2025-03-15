from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import routers as routes
import routers.auth as router_auth
from core.database import database
from core.translation import TranslationManager
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

# Autoriser le frontend Vue.js à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace "*" par "http://localhost:5173" en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TranslateMiddleware)

app.include_router(routes.users.router)
app.include_router(router_auth.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}