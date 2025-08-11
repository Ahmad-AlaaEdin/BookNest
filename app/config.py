import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
DB_NAME = os.getenv("DB_NAME")