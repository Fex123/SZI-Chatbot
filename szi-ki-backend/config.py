from dotenv import load_dotenv
import os

load_dotenv("../.env")

"""
Configuration settings for the Flask app
"""
class Config:
    DEBUG = False
    MONGO_URI = "mongodb://root:example@mongo:27017/"
    MONGO_DB_NAME = "dify_mongo"
    DIFY_URL = "http://docker-nginx-1/v1" # Local: http://docker-nginx-1/v1  Server: http://docker_nginx_1/v1
    DIFY_API_KEY = os.getenv('DIFY_API_KEY')  
    DIFY_HEADERS = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json'
    }
    TOP_QUERIES_UPDATE_INTERVAL = 3  # minutes
