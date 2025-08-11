from flask import Blueprint,render_template, request, redirect,session
from .models import User
from flask_login import login_required,current_user

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/user',methods=["PATCH"])

@main.route('/login')
def login():
    return render_template('login.html')



@main.route('/signup')
def signup():
    return render_template('signup.html')



@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@main.route('/profile')
@login_required
def profile():
    print(current_user.check_password("fdsf"))
    return render_template('profile.html',user=current_user)
   
