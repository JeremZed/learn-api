from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TranslateMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        """
            On récupère la lang de demandé par la requête pour la rendre disponible facilement
        """
        request.state.current_lang = request.app.translator.get_language(request)

        response = await call_next(request)

        return response