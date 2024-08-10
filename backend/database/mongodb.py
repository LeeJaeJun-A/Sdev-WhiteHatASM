import logging
from backend.config import MONGODB_LOCAL_URI, MONGODB_DOCKER_URI, MONGODB_DATABASE_NAME, IS_DOCKER
from pymongo import MongoClient
import gridfs

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongodb_uri: str = ""
db_name: str = MONGODB_DATABASE_NAME

if IS_DOCKER == "true":
    mongodb_uri = MONGODB_DOCKER_URI
else:
    mongodb_uri = MONGODB_LOCAL_URI

# 사용 중인 MongoDB URI와 데이터베이스 이름 로깅
logger.info(f"Connecting to MongoDB using URI: {mongodb_uri}")
logger.info(f"Using database: {db_name}")

mongo_client = MongoClient(mongodb_uri)
db = mongo_client.get_database(db_name)

# 각 컬렉션 로깅
cve_collection = db.get_collection("cve")
logger.info(f"Using collection: cve")

history_collection = db.get_collection("history")
logger.info(f"Using collection: history")

contact_collection = db.get_collection("contact")
logger.info(f"Using collection: contact")

# GridFS 로깅
fs = gridfs.GridFS(db)
logger.info("GridFS initialized")

