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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

