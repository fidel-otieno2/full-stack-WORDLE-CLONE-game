import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecret')
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/wordle')
    if database_url and 'sslmode' not in database_url:
        database_url += '?sslmode=require'
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
