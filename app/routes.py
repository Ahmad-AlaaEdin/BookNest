from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from .models.user import User
from flask_login import login_required, current_user, logout_user
from .utils import User_File_Handler
from werkzeug.security import generate_password_hash
from .models.book import Book
from app import db
from sqlalchemy import delete, update, select

handler = User_File_Handler("app/users.json")

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/user", methods=["DELETE"])
@login_required
def delete_user():
    handler.remove(current_user.id)
    logout_user()
    return redirect("/")


@main.route("/password", methods=["PATCH"])
@login_required
def update_password():
    password = request.form.get("password")
    new_password = request.form.get("newPassword")
    password_confirm = request.form.get("passwordConfirm")
    if not password or not new_password or not password_confirm:
        flash("Please Provide Old Password and New password")
        return redirect("/profile")
    if not current_user.check_password(password):
        flash("Old Password Not Correct")
        return redirect("/profile")
    if new_password != password_confirm:
        flash("New Password and Password Confirm Not Equal")
        return redirect("/profile")

    current_user.password_hash = generate_password_hash(new_password)
    handler.update(current_user)
    logout_user()
    flash("Please Relogin")
    return redirect("/login")


@main.route("/user", methods=["PATCH"])
@login_required
def update_name():
    name = request.form.get("name")

    if not name:
        flash("Please Provide Name")
        return redirect("/profile")

    current_user.name = name
    handler.update(current_user)
    return redirect("/profile")


@main.route("/login")
def login():
    return render_template("login.html")


@main.route("/signup")
def signup():
    return render_template("signup.html")


@main.route("/dashboard")
@login_required
def dashboard():
    books = db.session.query(Book).filter_by(user_id=current_user.id).all()

    books_dict = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "pages": book.pages,
            "status": book.status,
        }
        for book in books
    ]
    return render_template("dashboard.html",books=books_dict)


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@main.route("/books", methods=["POST"])
@login_required
def add_book():

    title = request.form.get("title")
    author = request.form.get("author")
    pages = request.form.get("pages")
    status = request.form.get("status")

    if not title or not author or not pages or not status:
        flash("All Fields Are Required")
        return redirect("/dashboard")
    new_book = Book(
        user_id=current_user.id, title=title, author=author, pages=pages, status=status
    )
    db.session.add(new_book)
    db.session.commit()
    return redirect("/dashboard")


@main.route("/books", methods=["DELETE"])
@login_required
def delete_book():

    book_id = request.form.get("book_id")

    if not book_id:
        flash("Book Id Required")
        return redirect("/dashboard")
    stm = select(Book).where(Book.id == book_id)

    book = db.session.get(Book, book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect("/dashboard")


@main.route("/books", methods=["GET"])
@login_required
def get_all_books():

    books = db.session.query(Book).filter_by(user_id=current_user.id).all()

    books_dict = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "pages": book.pages,
            "status": book.status,
        }
        for book in books
    ]
    return jsonify(books_dict)


@main.route("/books", methods=["PATCH"])
@login_required
def update_book():

    book_id = request.form.get("book_id")
    title = request.form.get("title")
    author = request.form.get("author")
    pages = request.form.get("pages")
    status = request.form.get("status")

    if not book_id:
        flash("Book Id Required")
        return redirect("/dashboard")
    stm = select(Book).where(Book.id == book_id).where(Book.user_id == current_user.id)

    book = db.session.get(Book, book_id)
    if not book or book.user_id != current_user.id:
        flash("Book not found or unauthorized")
        return redirect("/dashboard")

    if title:
        book.title = title

    if author:
        book.author = author

    if pages:
        book.pages = pages

    if status:
        book.status = status

    db.session.commit()
    return redirect("/dashboard")


"""
@main.route("/books", methods=["POST"])
@login_required
def add_book():
    title = request.form.get("title")
    author = request.form.get("author")
    pages = request.form.get("pages")
    status = request.form.get("status")

    if not title or not author or not pages or not status:
        flash("All Fields Are Required")
        return redirect("/dashboard")
    new_book = Book(
        user_id=current_user.id, title=title, author=author, pages=pages, status=status
    )
    db.session.add(new_book)
    db.session.commit()
    return redirect("/dashboard")
@main.route("/books", methods=["POST"])
@login_required
def add_book():
    title = request.form.get("title")
    author = request.form.get("author")
    pages = request.form.get("pages")
    status = request.form.get("status")

    if not title or not author or not pages or not status:
        flash("All Fields Are Required")
        return redirect("/dashboard")
    new_book = Book(
        user_id=current_user.id, title=title, author=author, pages=pages, status=status
    )
    db.session.add(new_book)
    db.session.commit()
    return redirect("/dashboard")



@main.route("/books",methods=["POST"])
@login_required
def add_book():
    
"""
