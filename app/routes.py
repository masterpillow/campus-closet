from flask import render_template, request, redirect, url_for, session
from app import app, db
from app.models import User, Listing

# 🌐 Landing page
@app.route('/')
def landing():
    return render_template('index.html')

# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Only allow SCSU emails
        if not email.endswith('@southernct.edu'):
            return "Only SCSU email addresses are allowed."

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "User already exists. Try logging in."

        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('routes.login'))  # redirect to login after signup

    return render_template('signup.html')

# 🔐 Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Only allow SCSU emails
        if not email.endswith('@southernct.edu'):
            return "Only SCSU email addresses are allowed."

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return "Login successful! "
        else:
            return "Invalid email or password."

    return render_template('login.html')

# 🏠 Home page
@app.route('/home')
def home():
    return render_template('home.html')

# ➕ Create a new listing
@app.route('/create-listing', methods=['GET', 'POST'])
def create_listing():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        category = request.form['category']
        user_id = session.get('user_id')
        listing = Listing(title=title, description=description, price=price, category=category, user_id=user_id)
        db.session.add(listing)
        db.session.commit()
        return redirect(url_for('listings'))
    return render_template('create_listing.html')

# 📋 View all listings
@app.route('/listings')
def listings():
    all_listings = Listing.query.all()
    return render_template('listings.html', listings=all_listings)