from flask import Blueprint, render_template, request, redirect, session, flash
from .models import User
from flask_login import login_required, current_user, logout_user
from .utils import User_File_Handler
from werkzeug.security import generate_password_hash

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
def dashboard():
    return render_template("dashboard.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
