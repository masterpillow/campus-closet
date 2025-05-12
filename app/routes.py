# routes.py
# This file defines the routes (URL endpoints) for the application
# It includes logic for user registration, login, messaging, favorites, item listings, and admin dashboard access
# Uses Flask Blueprints to modularize routes 

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, ItemListing, login_manager, Favorite, Message
from .forms import LoginForm, RegisterForm, ItemListingForm, MessageForm
from datetime import datetime 

bp = Blueprint('main', __name__)


# Route decorator binds a URL path to the following function
# View function that handles the request and returns a response 
@bp.route('/')
def landing():
    return render_template('index.html')

# Home page
# Route decorator binds a URL path to the following function
# View function that handles the request and returns a response
@bp.route('/home')
def home():
    listings = ItemListing.query.all()

    favorited_ids = [] 
    if current_user.is_authenticated:
        favorited_ids = [f.listing_id for f in current_user.favorites]

    return render_template('home.html', listings=listings, favorited_ids=favorited_ids)

# Signup
# Renders and processes the registration form
# Validates SCSU email, checks for duplicates, creates a new user
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        # Only accepts southern emails.
        if not form.email.data.endswith('@southernct.edu'):
            flash("Only SCSU email addresses are allowed.")
            return render_template('signup.html', form=form)

        # Redirects the user to the login page if the user email already is in use
        existing_user = User.query.filter_by(email=form.email.data).first() 
        if existing_user:
            return redirect(url_for('main.login'))

        # Set of emails that are keyed in for the role of an admin
        admin_emails = [
            "mastelarig1@southernct.edu",
            "garciar17@southernct.edu",
            "madhua1@southernct.edu",
            "muneerb1@southernct.edu",
            "musialm5@southernct.edu",
            "wrightj16@southernct.edu"
        ]
        is_admin = form.email.data in admin_emails
        
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            name=form.name.data, 
            email=form.email.data, 
            password=hashed_password,
            is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)

# Login
# Authenticates user credentials and logs user in
# Used hashed password check and redirects on success or failure 
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

# Logout
# Logs oyt current user and clears session 
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Create listing
# Form for submitting new item listings
# Saves listings metadata to database if validated 
@bp.route('/create_item_listing', methods=['GET', 'POST'])
@login_required
def create_item_listing():
    form = ItemListingForm()
    if form.validate_on_submit():
        listing = ItemListing(
            userID=current_user.id,
            userName=current_user.name,
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            condition=form.condition.data
        )
        db.session.add(listing)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('create_item_listing.html', form=form)

# View listing
@bp.route('/view_listing/<int:listingID>')
def view_listing(listingID):
    listing = ItemListing.query.get_or_404(listingID)
    user = User.query.filter_by(id=listing.userID).first()
    favorited_ids = []
    if current_user.is_authenticated:
        favorited_ids = [f.listing_id for f in current_user.favorites]
    return render_template('view_listing.html', listing=listing, user=user, favorited_ids=favorited_ids)

# Add to favorites
@bp.route('/favorite/<int:listing_id>', methods=['POST'])
@login_required
def favorite_listing(listing_id):
    existing = Favorite.query.filter_by(user_id=current_user.id, listing_id=listing_id).first()
    if not existing:
        fav = Favorite(user_id=current_user.id, listing_id=listing_id)
        db.session.add(fav)
        db.session.commit()
    return redirect(request.referrer or url_for('main.home'))

# Remove from favorites
@bp.route('/unfavorite/<int:listing_id>', methods=['POST'])
@login_required
def unfavorite_listing(listing_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, listing_id=listing_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
    return redirect(request.referrer or url_for('main.view_favorites'))

# View all favorites
# Displays listings the current user has favorited 
@bp.route('/favorites')
@login_required
def view_favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favorites)

# Messages page
# Shows all received messages for the logged-in user 
@bp.route('/messages')
@login_required
def messages():
    messages = Message.query.filter_by(receiverID=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('messages.html', messages = messages)

# Sending message route
# Promt the user to enter a message to send to the user of a particular listing
@bp.route('/message_user/<int:userID>', methods=['GET', 'POST'])
@login_required
def message_user(userID):
    user = User.query.filter_by(id=userID).first_or_404()
    message = None 
    form = MessageForm()
    if form.validate_on_submit():
        if not user: 
            message = "User not found." 
        else:
            msg = Message(senderID=current_user.id, receiverID=user.id, content=form.body.data)
            db.session.add(msg)
            db.session.commit()
            flash('Your message has been sent.')
            return redirect(url_for('main.messages'))
        
    return render_template('message_user.html', form=form, message=message, user=user)

# View details of a particular message
@bp.route('/view_message/<int:messageID>')
def view_message(messageID):
    message = Message.query.get_or_404(messageID)

    return render_template('view_message.html', message = message)

# View details of a particular message
@login_required
@bp.route('/user_profile>')
def user_profile():
    return render_template('user_profile.html')


# Admin dashboard
@bp.route("/admin")
@login_required
def admin_dashboard(): 
    if not current_user.is_admin:
        flash("Unauthorized access.")
        return redirect(url_for('main.home'))

    users = User.query.all()
    items = ItemListing.query.all()
    return render_template("admin_dashboard.html", users=users, items=items)
