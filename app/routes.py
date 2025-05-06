from flask import Blueprint, render_template, redirect, url_for, flash, request,session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, login_manager
from .forms import LoginForm, RegisterForm

bp = Blueprint('main', __name__)

# 🌐 Landing page
@bp.route('/')
def landing():
    return render_template('index.html')


# 🏠 Home page
@bp.route('/home')
def home():
    return render_template('home.html')

#Minor update: added comment to trigger pull request visibility
# signup route 
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if not form.email.data.endswith('@southernct.edu'):
            flash("Only SCSU email addresses are allowed.")
            return render_template('signup.html', form=form)

        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            return redirect(url_for('main.login'))

        hashed_password = generate_password_hash(form.password.data)
        user = User(name = form.name.data,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))  # redirect to login after signup
    
    return render_template('signup.html', form=form)

# 🔐 Login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('main.login'))
        
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))