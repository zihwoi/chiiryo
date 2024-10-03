from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from models import db # Import the db object
from routes import init_routes  # Import the init_routes function

load_dotenv()  # Load environment variables from .env

# No need to specify template_folder since it's the default
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# MySQL database configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

init_routes(app)  # Initialize routes    

if __name__ == '__main__':
    app.run(debug=True)

    