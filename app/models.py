# models.py
# This file defines the SQLAlchemy models for the application
# Each model corresponds to a table in the database and includes relationships and attributes

from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timezone

# Database model definition with fields and constraints
# User Model: represents application users
# Includes login credentials, profile info, and admin privileges 
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # primary key field 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # Users email address (must be unique)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50))
    major = db.Column(db.String(100))
    interests = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255))

    listings = db.relationship('ItemListing', backref='user', lazy=True)
    favorites = db.relationship('Favorite', back_populates='user', cascade="all, delete-orphan")

    # Boolean flag for admin privileges 
    is_admin = db.Column(db.Boolean, default=False)

# Database model definition with fields and constraints
# item Listing Model: represents a listing posted by a user
# Stores listing metadata like title, description, and category 
class ItemListing(db.Model):
    __tablename__ = 'listings'

    # Primary key field
    listingID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    userName = db.Column(db.String(100))
    title = db.Column(db.String(100))
    description = db.Column(db.Text) 
    category = db.Column(db.String(50))
    condition = db.Column(db.String(50))
    imageURL = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    favorites = db.relationship('Favorite', backref = 'Favorites', lazy = True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database model definition with fields and constraints
# Favorites model: tracks items a user has marked as favorite
# Enables relationships between users and listings 
class Favorite(db.Model):
    __tablename__ = 'favorites'

    # primary key field 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.listingID'), nullable=False)

    user = db.relationship('User', back_populates='favorites')
    ItemListing = db.relationship('ItemListing')

# Database model definition with fields and constraints
# Message model: stores direct messages between users
# Includes sender, receiver, content and timestamp 
class Message(db.Model):
    __tablename__ = 'messages'

    messageID = db.Column(db.Integer, primary_key=True)
    senderID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiverID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[senderID])
    receiver = db.relationship('User', foreign_keys=[receiverID])
