from . import db, login_manager
from flask_login import UserMixin

from datetime import datetime, timezone

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50))
    major = db.Column(db.String(100))
    interests = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255))

    listings = db.relationship('ItemListing', backref='user', lazy=True)
    favorites = db.relationship('Favorite', back_populates='user', cascade="all, delete-orphan")


class ItemListing(db.Model):
    __tablename__ = 'listings'

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

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.listingID'), nullable=False)

    user = db.relationship('User', back_populates='favorites')
    ItemListing = db.relationship('ItemListing')

class Message(db.Model):
    __tablename__ = 'messages'

    messageID = db.Column(db.Integer, primary_key=True)
    senderID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiverID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

