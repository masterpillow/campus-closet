from flask import render_template, request, redirect, url_for, session
from app import app, db
from app.models import User, Listing

# 🌐 Landing page
@app.route('/')
def landing():
    return render_template('index.html')

# 🔐 Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('home'))
        return "Invalid login"
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