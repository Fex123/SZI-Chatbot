from dotenv import load_dotenv
import os

load_dotenv("../.env")

class Config:
    DEBUG = True
    MONGO_URI = "mongodb://root:example@host.docker.internal:3106/"
    MONGO_DB_NAME = "dify_mongo"
    DIFY_URL = "http://host.docker.internal/v1"
    DIFY_API_KEY = os.getenv('DIFY_API_KEY')  
    DIFY_HEADERS = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json'
    }
