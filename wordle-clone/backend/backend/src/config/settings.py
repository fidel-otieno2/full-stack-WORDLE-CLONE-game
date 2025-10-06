# Database configuration for PostgreSQL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus #for URL encoding of the database passwrd

# PostgreSQL configuration
DB_USERNAME = os.getenv("DB_USERNAME", "postgres.szfyytdzcgljaesbwkri")
DB_PASSWORD = os.getenv("DB_PASSWORD", "CQ9A4@Axf?Hw-Z6")
DB_HOST = os.getenv("DB_HOST", "aws-1-eu-north-1.pooler.supabase.com")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

# URL-encode the password to handle special characters
encoded_password = quote_plus(DB_PASSWORD)
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create PostgreSQL engine and manages the the actual Database connection pool
engine = create_engine(SQLALCHEMY_DATABASE_URL) #according to our project all the ORM queries and operations will use this engine

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close() #ensures our database is to prevent data leakage

# Function to get database URL for Alembic
def get_database_url():
    """Return the database URL based on the current configuration."""
    return SQLALCHEMY_DATABASE_URL
