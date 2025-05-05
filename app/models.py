from flask_alchemy import SQLAlchemy
from datetime import datetime 

db = SQLAlchemy() 

class User(db.Model):
    __tablename__ = 'users'

    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50))
    major = db.Column(db.String(100))
    interests = db.Column(db.String.PickleType)
    profile_picture = db.Column(db.String(255))

    listings = db.relationship('ItemListing', backref='user', lazy=True)
    messages_sent = db.relationship('Message', foreign_keys='Message.senderID', backref='sender', lazy=True)
    messages_received = db.relationship('Message', foreign_keys = "Message.receiverID", backref='receiver', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    feedback_written = db.relationship('Feedback', foreign.keys'Feedback.reviewerID', backref='reviewer', lazy=True)
    feedback_receieved = db.relationship('Feedback', foreign_keys = 'Feedback.reviewerID', backref='reviewee', lazy=True)
    favorites = db.relationship('Favorite', backref = 'user', lazy = True)

class ItemListing(db.Model):
    __tablename__ = 'listings'

    listingID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    title = db.Column(db.String(100))
    description = db.Column(db.Text) 
    category = db.Column(db.String(50))
    condition = db.Column(db.String(50))
    status = db.Column(db.String(20))
    imageURL = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default = datetime.utcnow)


    favorites = db.relationship('Favorite', backref = 'listing', lazy=True)
    feedbacks = db.relationship('Feedback', backref = 'listing', lazy=True)

class Favorites(db.Model):
    __tablename__ = 'Favorites'

    favoritesID = db.Column(db.Integer, primary_keys=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    listingID = db.Column(db.Integer, db.ForeignKey('listings.listingID'), nullable=False)


class Message(db.Model):
    __tablename__ = 'messages'

    messageID = db.Column(db.Integer, primary_key=True)
    senderID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    receiverID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Notifcation(db.Model): 
    __tablename__ = 'notifications'

    notificationID= db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    message = db.Column(db.String(255))
    type = db.Column(db.String(50))
    isRead = db.Column(db.Boolean, default=False)
    timeStamp = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model): 
    __tablename__ = 'feedback'

    feedbackID = db.Column(db.Integer, primary_keys = True)
    reviewerID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    revieweeeID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    listingID = db.Column(db.Integer, db.ForeignKey('listings.listingID'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    dateSubmitted = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model): 
    __tablename__ = 'admins'

    adminID = db.Column(db.Integer, primary_keys = True)
    can_modertate = db.Column(db.Boolean, default=True)

class UsageStats(db.Model): 
    __tablename__ = 'usage_stats'

    statsID = db.Column(db.Integer, primary_key=True)
    totalUsers = db.Column(db.Integer)
    active_listings = db.Column(db.Integer)
    messages_sent = db.Column(db.Integer)
    reports_submitted = db.Column(db.Integer)






