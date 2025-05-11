from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, ItemListing, login_manager, Favorite, Message
from .forms import LoginForm, RegisterForm, ItemListingForm, MessageForm
from datetime import datetime 

bp = Blueprint('main', __name__)

# 🌐 Landing page
@bp.route('/')
def landing():
    return render_template('index.html')

# Home page
@bp.route('/home')
def home():
    listings = ItemListing.query.all()

    favorited_ids = []
    if current_user.is_authenticated:
        favorited_ids = [f.listing_id for f in current_user.favorites]

    return render_template('home.html', listings=listings, favorited_ids=favorited_ids)

# Signup
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
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)

# Login
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
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Create listing
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
@bp.route('/favorites')
@login_required
def view_favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favorites)

# Messages page
@bp.route('/messages')
@login_required
def messages():
    messages = Message.query.filter_by(receiverID=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('messages.html', messages = messages)

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

# View message 
@bp.route('/view_message/<int:messageID>')
def view_message(messageID):
    message = Message.query.get_or_404(messageID)

    return render_template('view_message.html', message = message)

#  email: muneerb1
# password: ssbb