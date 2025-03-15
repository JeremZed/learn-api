import aiohttp
import json
from loguru import logger

class Client():

    def __init__(self, options:dict):
        self.host = options.get('host', '127.0.0.1')
        self.port = options.get('port', 80)
        self.protocol = options.get('protocol', 'http')
        self.headers = options.get('headers', None)

        self.base_url = f"{self.protocol}://{self.host}:{self.port}"
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
            self.session = None

    async def query(self, method: str, endpoint: str, headers: dict = None, **kwargs):
        """
        Effectue une requête HTTP asynchrone.
        """

        if not self.session:
            raise RuntimeError("Client session not initialized. Use 'async with Client()' or call 'await client.__aenter__()' before making requests.")

        url = f"{self.base_url}{endpoint}"
        headers = headers or self.headers
        try:
            async with self.session.request(method.upper(), url, headers=headers, **kwargs) as response:

                try:
                    response.raise_for_status()
                except aiohttp.ClientResponseError:
                    try:
                        error_json = await response.json()
                        error_message = error_json.get("detail", "Unknown error")

                    except aiohttp.ContentTypeError:
                        error_message = await response.text()

                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=error_message
                    )

                if 'application/json' in response.headers.get('Content-Type', ''):
                    return await response.json()
                return await response.text()


        except aiohttp.ClientResponseError as e:
            logger.error(f"API Error ({e.status}): {e.message}")
            return None

        except aiohttp.ClientError as e:
            logger.error(f"HTTP Request Error: {e}")
            return None

    async def login(self, email, password):
        """
            Permet de lancer une requête d'authentification
        """

        data = {
            "email": email,
            "password" : password,
        }

        response = await self.query(method='POST', endpoint="/auth/login", json=data)

        if response:
            self.headers['Authorization'] = f"{response.get('data').get('token_type')} {response.get('data').get('token')}"

        return response



