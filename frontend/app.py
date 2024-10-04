from flask import Flask, send_from_directory
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from routes import init_routes  # Import routes

load_dotenv()  # Load environment variables from .env

# Initialize Flask app
app = Flask(__name__, static_folder='frontend/build/static', static_url_path='/static')
app.secret_key = 'your_secret_key'  # Replace with a secure key

# MySQL database configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Route to serve the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    return send_from_directory('frontend/build', 'index.html')

# Initialize additional routes
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
