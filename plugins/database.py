import pymongo
from config import MONGODB, DATABASE_NAME, COLLECTION_NAME
import ssl

URI = MONGODB
db = pymongo.MongoClient(URI, ssl_cert_reqs=ssl.CERT_NONE)
client = db[DATABASE_NAME]
collection = client[COLLECTION_NAME]

