from flask import Flask, jsonify, send_from_directory, abort
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from models import db # Import the db object
from routes import init_routes  # Import the init_routes function
from flask_cors import CORS
from flask_login import LoginManager

load_dotenv()  # Load environment variables from .env

# No need to specify template_folder since it's the default
# app = Flask(__name__)
app = Flask(__name__, static_folder='frontend/build/static', static_url_path='/static')  # Set static folder for React
app.secret_key = 'your_secret_key'  # Needed for flashing messages
CORS(app)  # This enables CORS for all routes

# MySQL database configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)
login_manager = LoginManager()  # Create the LoginManager instance
login_manager.init_app(app)  # Pass the app instance to the LoginManager


# Initialize routes
init_routes(app)  # Initialize routes

# Route to serve the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path and path.startswith('api'):
        # Let the API routes handle the request
        abort(404)  # or simply return None, but abort is cleaner
    try:
        return send_from_directory('frontend/build', path)
    except FileNotFoundError:
        # If the file isn't found, serve the React app's index.html
        return send_from_directory('frontend/build', 'index.html')

# # Import routes after db initialization to prevent circular import
# from routes import init_routes  # Moved here to avoid circular import
# init_routes(app)  # Initialize routes    

if __name__ == '__main__':
    app.run(debug=True)

    