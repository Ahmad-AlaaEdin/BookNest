from flask import Blueprint, request, flash, redirect
from .models import User

from .utils import User_File_Handler

from flask_login import login_user, logout_user

handler = User_File_Handler("app/users.json")
auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    if not name or not email or not password:
        flash("Both Username and Password Required")
        return redirect("/signup")
    usr = handler.get_by_email(email)
    if usr:
        flash("User Name Already Exist", "error")
        return redirect("/signup")
    user = User.create(name, email, password)
    handler.add(user)
    flash("Signup Succed")
    return redirect("/signup")


@auth.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        flash("Both Username and Password Required")
        return redirect("/login")

    print(email)
    usr = handler.get_by_email(email)
    if usr:
        print("found")
        
        if usr.check_password(password):
            login_user(usr)
            flash("logged in succesfully")
            return redirect("/dashboard")
        flash("Invalid Username or Password ")
    else:
        flash("User Not Found")

    return redirect("/login")


@auth.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect("/login")
