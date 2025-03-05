from bson import ObjectId
from datetime import datetime, timezone

class BaseRepository:
    def __init__(self, db, entity):
        self.collection = db.get_collection(entity)

    async def get_all(self, skip: int, limit: int):
        return await self.collection.find().skip(skip).limit(limit).to_list(length=None)

    async def get_by_id(self, id: str):
        return await self.collection.find_one({"_id": ObjectId(id)})

    async def create(self, data: dict):
        return await self.collection.insert_one(data)

    async def update(self, id: str, update_data: dict):
        return await self.collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    async def soft_delete(self, id: str):
        return await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"deleted_at": datetime.now(timezone.utc)}}
        )
    async def hard_delete(self, id: str):
        return await self.collection.delete_one({"_id": ObjectId(id)})
