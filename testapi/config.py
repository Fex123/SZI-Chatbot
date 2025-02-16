class Config:
    DEBUG = True
    MONGO_URI = "mongodb://root:example@localhost:27017/"
    MONGO_DB_NAME = "test_db"
    DIFY_URL = "http://localhost/v1"
    DIFY_API_KEY = "app-Ea0MYTfWhjxI4cf7lSlI3ErD"
    DIFY_HEADERS = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json'
    }
