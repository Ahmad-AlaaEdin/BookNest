from flask import Blueprint,render_template, request, redirect
from .utils import Text_File_Handler
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')



@main.route('/login')
def login():
    return render_template('login.html')



@main.route('/signup')
def signup():
    return render_template('signup.html')



@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
