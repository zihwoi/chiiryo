from flask import Flask, jsonify, request, send_from_directory, abort
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import db, User, Project, Milestone, Task # Import the db object
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

load_dotenv()  # Load environment variables from .env

# No need to specify template_folder since it's the default
# app = Flask(__name__)
app = Flask(__name__, static_folder='frontend/build/static', static_url_path='/static')

app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Enable CORS for your Flask app
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}) # Allow requests from React frontend


# MySQL database configuration using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)
login_manager = LoginManager()  # Create the LoginManager instance
login_manager.init_app(app)  # Pass the app instance to the LoginManager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create the database tables
with app.app_context():
    db.create_all()  # This creates all the tables if they don't already exist

# Home route
@app.route('/')
def home():
    return jsonify(message="Welcome to the API")

# User registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'All fields are required!'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'message': 'User already exists!'}), 409

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

    # User login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Both email and password are required!'}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Login successful!"}), 200

    return jsonify({'message': 'Login failed. Check your credentials.'}), 401

# User logout
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "You have been logged out."}), 200

# Get user info (protected route)
@app.route('/api/user', methods=['GET'])
@login_required
def get_user_info():
    return jsonify({
        "username": current_user.username,
        "message": "This is your profile data."
    })
# Get all projects
@app.route('/api/projects', methods=['GET'])
@login_required
def get_projects():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 14, type=int)  # Allow per_page parameter
    projects = Project.query.paginate(page=page, per_page=per_page)
    return jsonify([project.to_dict() for project in projects.items]), 200

# Create a new project
@app.route('/api/projects', methods=['POST'])
@login_required
def create_project():
    data = request.get_json()
    title = data['title']
    description = data['description']

    if not title or not description:
        return jsonify({"message": "Title and description are required."}), 400

    try:
        new_project = Project(title=title, description=description, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        return jsonify({"message": "Project created successfully!"}), 201
    
    except Exception as e:
        return jsonify({"message": "An error occurred while creating the project.", "error": str(e)}), 500

# Update project
@app.route('/api/projects/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json()

    if not data or 'title' not in data or 'description' not in data:
        return jsonify({"error": "Invalid input"}), 400

    project.title = data['title']
    project.description = data['description']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Project updated successfully!", "project": project.serialize()}), 200

# Delete project
@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()

    return jsonify({"message": "Project deleted successfully!"}), 200

# Handle CORS preflight requests
@app.route('/api/projects/<int:project_id>', methods=['OPTIONS'])
def options_project(project_id):
    return jsonify({"message": "CORS preflight response"}), 200

# Serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path and path.startswith('api'):
        abort(404)
    try:
        return send_from_directory('frontend/build', path)
    except FileNotFoundError:
        return send_from_directory('frontend/build', 'index.html')

# About route
@app.route('/api/about')
def about():
    fun_activities = [
        "creating interactive web applications.",
        "building fun games to play online.",
        "designing beautiful user interfaces.",
        "exploring new technologies and tools.",
        "collaborating with creative minds."
    ]
    return jsonify(fun_activities=fun_activities)

# Contact route
@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    return jsonify({"message": f"Thank you, {name}! Your message has been sent."}), 200


if __name__ == '__main__':
    app.run(debug=True)

    