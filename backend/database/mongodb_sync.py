from backend.config import MONGODB_URL
from pymongo import MongoClient
import gridfs

client = MongoClient(MONGODB_URL)

db = client.core_db

cve_collection = db.cve
fs = gridfs.GridFS(db)