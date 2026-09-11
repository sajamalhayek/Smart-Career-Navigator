import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    MODEL_NAME = os.getenv('MODEL_NAME', 'meta-llama/llama-3.3-70b-instruct:free')
    DATABASE_URI = 'sqlite:///database/app.db'