from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash,
    jsonify,
    abort,
)
from .models.user import User
from flask_login import login_required, current_user, logout_user
from .utils import User_File_Handler
from werkzeug.security import generate_password_hash
from .models.book import Book
from .models.note import Note
from app import db
from sqlalchemy import delete, update, select
from sqlalchemy.orm import joinedload

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
    image = request.form.get("image", "/static/images/default.png")
    if not title or not author or not pages or not status:
        return jsonify(message="All Fields Required"), 400

    new_book = Book(
        user_id=current_user.id,
        title=title,
        author=author,
        pages=pages,
        image=image,
        status=status,
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(message="Book Added Succesfuly"), 200


@main.route("/books/<int:book_id>", methods=["GET"])
@login_required
def get_book(book_id):
    book = (
        db.session.query(Book)
        .options(joinedload(Book.notes))
        .filter_by(id=book_id, user_id=current_user.id)
        .first()
    )
    if not book:
        abort(404, description="Book not found")

    print(book.notes)
    return render_template("book.html", book=book)


@main.route("/books/<int:book_id>/notes", methods=["POST"])
@login_required
def add_note(book_id):
    data = request.get_json()
    content = data.get("content") if data else None

    if not content:
        return jsonify(message="Content Required"), 400

    new_note = Note(
        book_id=book_id,
        content=content,
    )
    db.session.add(new_note)
    db.session.commit()

    note_dict = {
        "id": new_note.id,
        "content": new_note.content,
        "created_at": (
            new_note.created_at.strftime("%b %d, %Y") if new_note.created_at else ""
        ),
    }
    return jsonify(note_dict), 200


@main.route("/notes/<int:note_id>", methods=["DELETE"])
@login_required
def delete_note(note_id):

    if not note_id:
        return jsonify(message="Note Not Found"), 404

    stm = select(Note).where(Note.id == note_id)

    note = db.session.get(Note, note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify(message="Deleted successfully"), 201
    return jsonify(message="Note Not Found"), 404


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
