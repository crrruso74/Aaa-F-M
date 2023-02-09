import os

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OWNER_ID = int(os.environ.get("OWNER_ID"))
PORT = os.environ.get("PORT", "8080")

ADMINS = list(int(i) for i in os.environ.get("ADMINS", "").split(" ")) if os.environ.get("ADMINS") else []

if OWNER_ID not in ADMINS:
    ADMINS.append(OWNER_ID)

MONGODB = os.environ.get('MONGODB')
DATABASE_NAME = os.environ.get('DATABASE_NAME') 
COLLECTION_NAME = os.environ.get('COLLECTION_NAME')

UPDATE_CHANNEL =  os.environ.get('UPDATE_CHANNEL')
USERNAME = UPDATE_CHANNEL

RESULTS_COUNT = int(os.environ.get('RESULT_COUNTS', 20))

AUTO_DELETE = os.environ.get('AUTO_DELETE', False)
AUTO_DELETE_TIME = int(os.environ.get('AUTO_DELETE_TIME', 600))
IMDB_TEMPLATE = os.environ.get("IMDB_TEMPLATE", "<b>Query: {query}</b> \n‌IMDb Data:\n\n🏷 Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n📆 Year: <a href={url}/releaseinfo>{year}</a>\n🌟 Rating: <a href={url}/ratings>{rating}</a> / 10")
MAX_LIST_ELM = os.environ.get("MAX_LIST_ELM", None)

