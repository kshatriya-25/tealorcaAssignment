# OM VIGHNHARTAYE NAMO NAMAH :

import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / '.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print("Warning: .env file not found. Environment variables may not be loaded.")

class Settings:

    PROJECT_NAME : str = "ENWISE"
    PROJECT_VERSION = "0.0.1"
    
    APP_ENV = os.getenv("APP_ENV")
    # ADMIN_PORTAL = os.getenv("ADMIN_PORTAL_HOST")


    # SERVER_URL : str = os.getenv('SERVER_URL') 
    # Upload directories
    UPLOAD_BASE_DIR = "uploads"  # Base directory for all uploads
    LOGO_DIR = os.path.join(UPLOAD_BASE_DIR, "logos")  # Subdirectory for logos
    DOCUMENT_DIR = os.path.join(UPLOAD_BASE_DIR, "documents")  # Subdirectory for documents

    THUMBNAIL_DIR = "uploads/logo_imgs"
    SITE_DOCUMENT_DIR = "uploads/site_documents"
 
    DB_USER : str = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST : str = os.getenv("DB_HOST")
    DB_PORT : str = os.getenv("DB_PORT",5432) # default postgres port is 5432
    DB_NAME : str = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 90  # 90 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
    ALGORITHM : str = os.getenv('ALGORITHM', 'HS256')
    JWT_SECRET_KEY : str = os.getenv('JWT_SECRET_KEY')   # should be kept secret
    JWT_REFRESH_SECRET_KEY : str = os.getenv('JWT_REFRESH_SECRET_KEY')   # should be kept secret
    
settings = Settings()