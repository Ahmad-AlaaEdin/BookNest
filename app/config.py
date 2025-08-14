import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
DB_CON = os.getenv("DB_CON")