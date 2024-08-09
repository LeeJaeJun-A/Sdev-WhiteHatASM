from backend.config import MONGODB_URL
from pymongo import MongoClient

client = MongoClient(MONGODB_URL)

db = client.core_db

cve_collection = db.cve
report_collection = db.report