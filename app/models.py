from app import db
from werkzeug.security import generate_password_hash, check_password_hash  # Sana: For secure password handling

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
# Note to team: These methods allow us to safely store and check user passwords 
    # using hashing instead of plain text. Used in signup/login routes.
    # Hash the password before storing it in the database
    #Secure user model for login/signup feature – comment added to ensure PR visibility

    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Check hashed password during login
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)