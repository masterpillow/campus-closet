# run.py
# This script is the entry point of the Flask application
# It imports the app factory and runs the app in development mode

# Import the app factory function from the app package 
from app import create_app

# Create an instance of the Flask app using the factory function
app = create_app()

# Run the app if this script is executed directly 
if __name__ == '__main__':
    app.run(debug=True)
