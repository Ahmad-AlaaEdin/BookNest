from flask import Flask, render_template
from flask_login import LoginManager
from .utils import User_File_Handler
from .config import SECRET_KEY, DB_CON
from flask_sqlalchemy import SQLAlchemy

from app.models.book import Book
from app.models.note import Note
from app.models.base import Base

db = SQLAlchemy(model_class=Base)
handler = User_File_Handler("app/users.json")


def create_app():
    app = Flask("BookNest", template_folder="app/templates", static_folder="app/static")
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_CON
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return (
            render_template(
                "error.html",
                code=401,
                title="Unauthorized",
                message="You must log in to access this page.",
            ),
            401,
        )

    @login_manager.user_loader
    def load_user(user_id):
        user = handler.get(user_id)
        if user:
            return user
        return None

    from .routes.users import users
    from .routes.auth import auth
    from .routes.books import books
    from .routes.notes import notes
    from .routes.views import views

    app.register_blueprint(users)
    app.register_blueprint(auth)
    app.register_blueprint(books)
    app.register_blueprint(notes)
    app.register_blueprint(views)

    @app.errorhandler(404)
    def not_found(error):
        return (
            render_template(
                "error.html",
                code=404,
                title="Not Found",
            ),
            404,
        )

    return app
