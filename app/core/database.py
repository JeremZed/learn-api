from motor.motor_asyncio import AsyncIOMotorClient

from core.config import get_settings

setting = get_settings()

class Database:
    def __init__(self, uri: str, db: str):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(uri)
        self.db = self.client[db]

    async def connect(self):
        print("Connecting to MongoDB...")

    async def disconnect(self):
        self.client.close()
        print("Disconnected from MongoDB.")

database = Database(setting.MONGO_URI, setting.DB_NAME)
