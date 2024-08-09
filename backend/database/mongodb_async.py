from backend.config import MONGODB_URL
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(MONGODB_URL)
db = client.user_activity

history_collection = db.history
