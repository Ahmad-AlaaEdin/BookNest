from flask import Blueprint, request, jsonify, render_template, abort
from ..models.book import Book
from flask_login import login_required, current_user
from app import db
from sqlalchemy.orm import joinedload
from ..models.note import Note

books = Blueprint("books", __name__, url_prefix="/books")


@books.route("/", methods=["POST"])
@login_required
def add_book():

    title = request.form.get("title").strip()
    author = request.form.get("author").strip()
    pages = request.form.get("pages").strip()
    status = request.form.get("status").strip()
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


@books.route("/<int:book_id>", methods=["GET"])
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

    return render_template("book.html", book=book)


@books.route("/<int:book_id>/notes", methods=["POST"])
@login_required
def add_note(book_id):
    data = request.get_json()
    content = data.get("content") if data else None

    if not content.strip():
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


@books.route("/<int:book_id>", methods=["DELETE"])
@login_required
def delete_book(book_id):

    book = db.session.get(Book, book_id)
    if not book or book.user_id != current_user.id:

        return (
            jsonify(
                message="Book not found or you do not have permission to update it."
            ),
            404,
        )

    if book:
        db.session.delete(book)
        db.session.commit()
    return jsonify(message="Deleted"), 201


@books.route("/", methods=["GET"])
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


@books.route("/<int:book_id>", methods=["PUT"])
@login_required
def update_book(book_id):

    title = request.form.get("title").strip()
    author = request.form.get("author").strip()
    pages = request.form.get("pages").strip()
    status = request.form.get("status").strip()
    image = request.form.get("image").strip()
    book = db.session.get(Book, book_id)
    if not book or book.user_id != current_user.id:

        return (
            jsonify(
                message="Book not found or you do not have permission to update it."
            ),
            404,
        )

    if title:
        book.title = title

    if author:
        book.author = author

    if pages:
        book.pages = pages

    if status:
        book.status = status
    if image:
        book.image = image

    db.session.commit()
    return jsonify(message="Book updated successfully!"), 200
