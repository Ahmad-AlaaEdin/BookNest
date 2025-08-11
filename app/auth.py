from flask import Blueprint, request, jsonify, session, flash, redirect, url_for
from .models import User
from pydantic import ValidationError
from functools import wraps
from flask_login import login_manager
from .utils import User_File_Handler

from flask_login import login_user, logout_user

handler = User_File_Handler("app/users.json")
auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        flash("Both Username and Password Required")
        return redirect("/signup")
    usr = handler.get_by_username(username)
    if usr:
        flash("User Name Already Exist", "error")
        return redirect("/signup")
    user = User.create(username, password)
    handler.add(user)
    flash("Signup Succed")
    return redirect("/signup")


@auth.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        flash("Both Username and Password Required")
        return redirect("/login")

    print(username)
    usr = handler.get_by_username(username)
    if usr:
        print("found")
        user = User( usr["username"], usr["password_hash"])
        if user.check_password(password):
            login_user(user)
            flash("logged in succesfully")
            return redirect("/dashboard")

    flash("Invalid Username or Password ")
    return redirect("/login")


@auth.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect("/login")
