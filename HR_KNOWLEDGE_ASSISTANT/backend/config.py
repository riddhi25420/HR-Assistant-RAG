from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR=Path(__file__).resolve().parent
load_dotenv(BASE_DIR /".env")

class Config:
    APP_NAME=os.getenv("APP_NAME")
    ORACLE_HOST=os.getenv("ORACLE_HOST")
    ORACLE_PORT=int(os.getenv("ORACLE_PORT"))
    ORACLE_SERVICE=os.getenv("ORACLE_SERVICE")
    ORACLE_USER=os.getenv("ORACLE_USER")
    ORACLE_PASSWORD=os.getenv("ORACLE_PASSWORD")
    OLLAMA_MODEL=os.getenv("OLLAMA_MODEL")