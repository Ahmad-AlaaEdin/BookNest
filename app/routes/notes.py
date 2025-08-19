from flask import Blueprint, request, jsonify
from flask_login import login_required,current_user
from ..models.note import Note
from app import db

notes = Blueprint("notes", __name__, url_prefix="/notes")


@notes.route("/<int:note_id>", methods=["DELETE"])
@login_required
def delete_note(note_id):

    if not note_id:
        return jsonify(message="Note Not Found"), 404

    note = db.session.get(Note, note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify(message="Deleted successfully"), 201
    return jsonify(message="Note Not Found"), 404


@notes.route("/<int:note_id>", methods=["PUT"])
@login_required
def update_note(note_id):
    data = request.get_json()
    new_content = data.get("content").strip()
    if not new_content:
        return jsonify(message="Content Required"), 400

    note = db.session.get(Note, note_id)
    if not note or note.book.user_id != current_user.id:
        return jsonify(message="Note Not Found"), 404

    note.content = new_content
    db.session.commit()

    return (
        jsonify(
            {
                "id": note.id,
                "content": note.content,
                "message": "Note updated successfully",
            }
        ),
        200,
    )
