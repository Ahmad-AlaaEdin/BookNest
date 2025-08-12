from flask import Flask
from flask_login import LoginManager
from .utils import User_File_Handler
from .models import User
from .config import SECRET_KEY

handler = User_File_Handler("app/users.json")


def create_app():
    app = Flask("BookNest", template_folder="app/templates", static_folder="static")
    app.secret_key = SECRET_KEY
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = handler.get(user_id)
        if user:
            return user
        return None

    from .routes import main
    from .auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
