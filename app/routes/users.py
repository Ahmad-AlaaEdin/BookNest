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
from ..models.user import User
from flask_login import login_required, current_user, logout_user
from ..utils import User_File_Handler
from werkzeug.security import generate_password_hash
from ..models.book import Book
from ..models.note import Note

from sqlalchemy import delete, update, select
from sqlalchemy.orm import joinedload

handler = User_File_Handler("app/users.json")

users = Blueprint("users", __name__)




@users.route("/user", methods=["DELETE"])
@login_required
def delete_user():
    handler.remove(current_user.id)
    logout_user()
    return redirect("/")


@users.route("/password", methods=["PATCH"])
@login_required
def update_password():

    password = request.form.get("old-password")
    new_password = request.form.get("new-password")
    password_confirm = request.form.get("password-confirm")

    if not password or not new_password or not password_confirm:
        return jsonify(message="Please provide old password and new password"), 400

    if not current_user.check_password(password):
        return jsonify(message="Old password is not correct"), 401

    if new_password != password_confirm:
        return jsonify(message="New password and confirmation do not match"), 400

    current_user.password_hash = generate_password_hash(new_password)
    handler.update(current_user)
    logout_user()

    return jsonify(message="Password updated successfully. Please relogin."), 200


@users.route("/user", methods=["PATCH"])
@login_required
def update_name():
    name = request.form.get("name", "").strip()

    if not name:
        return jsonify(message="Please provide Name"), 400

    current_user.name = name
    handler.update(current_user)

    return jsonify(message="Name updated successfully."), 200



