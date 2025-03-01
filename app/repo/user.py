from bson import ObjectId
from datetime import datetime, timezone

class UserRepository:
    def __init__(self, db):
        self.collection = db.get_collection("users")

    async def get_all_users(self, skip: int, limit: int):
        return await self.collection.find().skip(skip).limit(limit).to_list(length=None)

    async def get_user_by_id(self, user_id: str):
        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def check_email_exists(self, email: str):
        return await self.collection.find_one({"email": email})

    async def create_user(self, user_data: dict):
        return await self.collection.insert_one(user_data)

    async def update_user(self, user_id: str, update_data: dict):
        return await self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    async def soft_delete_user(self, user_id: str):
        return await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"deleted_at": datetime.now(timezone.utc)}}
        )
