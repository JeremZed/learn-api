from bson import ObjectId
from datetime import datetime, timezone
from repo.base import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, "users")

    async def check_email_exists(self, email: str):
        return await self.collection.find_one({"email": email})

    async def check_token_reset_password(self, email: str, token: str):
        return await self.collection.find_one({"email": email, 'token_password' : token})