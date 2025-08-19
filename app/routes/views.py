from flask import Blueprint, render_template,request
from flask_login import login_required
from app import db
from sqlalchemy import select
from flask_login import current_user
from ..models.book import Book
views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/login")
def login():
    return render_template("login.html")


@views.route("/signup")
def signup():
    return render_template("signup.html")


@views.route("/dashboard")
@login_required
def dashboard():
    title = request.args.get("title")
    status = request.args.get("status")
    stmt = select(Book).filter_by(user_id=current_user.id)
    if title:
        stmt = stmt.filter(Book.title.ilike(f"%{title}%"))
    if status:
        stmt = stmt.filter_by(status=status)

    books = db.session.scalars(stmt).all()

    books_dict = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "pages": book.pages,
            "image": book.image,
            "status": book.status,
        }
        for book in books
    ]
    return render_template("dashboard.html", books=books_dict)


@views.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
