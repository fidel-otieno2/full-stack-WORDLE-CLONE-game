import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/wordle')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
