from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv()

def create_app():
    app = Flask("BookNest",template_folder='app/templates', static_folder='static')
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    from .routes import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

   
    return app