from flask import jsonify, request, flash, redirect, url_for
from models import db, User, Project
from werkzeug.security import generate_password_hash, check_password_hash

def init_routes(app):
    @app.route('/api/register', methods=['POST'])
    def register():
        username = request.json.get('username')
        password = request.json.get('password')
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registration successful!'}), 201

    @app.route('/api/login', methods=['POST'])
    def login():
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Here, you can return a JWT or some form of session token
            return jsonify({'message': 'Login successful!'}), 200
        return jsonify({'message': 'Invalid username or password.'}), 401

    @app.route('/api/projects', methods=['GET', 'POST'])
    def manage_projects():
        if request.method == 'POST':
            project_title = request.json.get('project_title')
            project_description = request.json.get('project_description')
            new_project = Project(title=project_title, description=project_description, user_id=1)  # Update with actual user ID
            db.session.add(new_project)
            db.session.commit()
            return jsonify({'message': 'Project created successfully!'}), 201

        projects = Project.query.all()
        return jsonify([{'title': p.title, 'description': p.description} for p in projects]), 200
