from flask import jsonify, request, render_template, flash, redirect, url_for
from models import db, User, Project, Milestone, Task
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user



def init_routes(app):
    # Home route (if needed, can still render HTML or redirect)
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

        # Basic validation to check if the fields are provided
        if not username or not email or not password:
            return jsonify({'message': 'All fields are required!'}), 400

        # Check if user already exists
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

        # Basic validation to check if the fields are provided
        if not email or not password:
            return jsonify({'message': 'Both email and password are required!'}), 400

        user = User.query.filter_by(email=email).first()  # Corrected to filter by email
        if user and user.check_password(password):
            login_user(user)  # Login the user using Flask-Login
            return jsonify({"message": "Login successful!"}), 200

        return jsonify({'message': 'Login failed. Check your credentials.'}), 401
        
     # User logout
    @app.route('/api/logout', methods=['POST'])
    @login_required
    def logout():
        logout_user()
        return jsonify({"message": "You have been logged out."}), 200

    # API to get user info (protected route)
    @app.route('/api/user', methods=['GET'])
    @login_required
    def get_user_info():
        return jsonify({
            "username": current_user.username,
            "message": "This is your profile data."
        })

    # API for managing projects
    @app.route('/api/projects', methods=['GET', 'POST'])
    def manage_projects():
        if request.method == 'POST':
            data = request.get_json()
            title = data['title']
            description = data['description']

            new_project = Project(title=title, description=description, user_id=current_user.id)
            db.session.add(new_project)
            db.session.commit()
            return jsonify({"message": "Project created successfully!"}), 201

        page = request.args.get('page', 1, type=int)
        projects = Project.query.paginate(page=page, per_page=14)
        return jsonify([project.to_dict() for project in projects.items]), 200  # Assuming to_dict() method exists

    @app.route('/api/projects/<int:project_id>', methods=['PUT'])
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
            # Handle exceptions (e.g., database errors)
            db.session.rollback()  # Roll back the session in case of an error
            return jsonify({"error": str(e)}), 500
        
         # Return the updated project as a response
        return jsonify({"message": "Project updated successfully!", "project": project.serialize()}), 200

    # API for deleting a project
    @app.route('/api/projects/<int:project_id>', methods=['DELETE'])
    @login_required
    def delete_project(project_id):
        project = Project.query.get_or_404(project_id)

        db.session.delete(project)
        db.session.commit()

        return jsonify({"message": "Project deleted successfully!"}), 200


    # OPTIONS route to handle CORS preflight requests
    @app.route('/api/projects/<int:project_id>', methods=['OPTIONS'])
    def options_project(project_id):
        return jsonify({"message": "CORS preflight response"}), 200

    # About route (if needed, can still render HTML or return JSON)
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

    # Contact route (you can change to handle JSON requests)
    @app.route('/api/contact', methods=['POST'])
    def contact():
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # You can handle the message (store it, send an email, etc.)
        # Here we just return a success message
        return jsonify({"message": f"Thank you, {name}! Your message has been sent."}), 200

#serving the html loading of the app
# def init_routes(app):
#     @app.route('/')
#     def home():
#         return render_template('index.html')

#     @app.route('/about')
#     def about():
#         fun_activities = [
#             "creating interactive web applications.",
#             "building fun games to play online.",
#             "designing beautiful user interfaces.",
#             "exploring new technologies and tools.",
#             "collaborating with creative minds."
#         ]
#         return render_template('about.html', fun_activities=fun_activities)

#     @app.route('/contact', methods=['GET', 'POST'])
#     def contact():
#         if request.method == 'POST':
#             name = request.form['name']
#             email = request.form['email']
#             message = request.form['message']
#             flash(f"Thank you, {name}! Your message has been sent.")
#             return render_template('contact.html')
#         return render_template('contact.html')

#     @app.route('/register', methods=['GET', 'POST'])
#     def register():
#         if request.method == 'POST':
#             username = request.form['username']
#             password = request.form['password']
#             hashed_password = generate_password_hash(password)

#             new_user = User(username=username, password=hashed_password)
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Registration successful! Please log in.')
#             return redirect(url_for('login'))

#         return render_template('register.html')

#     @app.route('/login', methods=['GET', 'POST'])
#     def login():
#         if request.method == 'POST':
#             username = request.form['username']
#             password = request.form['password']
#             user = User.query.filter_by(username=username).first()

#             if user and check_password_hash(user.password, password):
#                 # Logic to generate and return JWT can be added here
#                 flash('Login successful!')
#                 return redirect(url_for('manage_projects'))  # Redirect to projects page

#             flash('Invalid username or password.')

#         return render_template('login.html')

#     @app.route('/api/projects', methods=['GET', 'POST'])
#     def manage_projects():
#         if request.method == 'POST':
#             project_title = request.form['project_title']
#             project_description = request.form['project_description']
#             user_id = 1  # Replace this with the actual logged-in user's ID

#             new_project = Project(title=project_title, description=project_description, user_id=1)  # Replace 1 with the logged-in user's ID

#             db.session.add(new_project)
#             db.session.commit()
            
#             flash('Project created successfully!')
#             return redirect(url_for('manage_projects'))

#         #projects = Project.query.all()
#         page = request.args.get('page', 1, type=int)
#         projects = Project.query.paginate(page=page, per_page=8)  # Show 8 projects per page
#         return render_template('projects.html', projects=projects)

#     @app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
#     def edit_project(project_id):
#         project = Project.query.get_or_404(project_id)  # Fetch the project by ID
    
#         if request.method == 'POST':
#             # Logic to update the project
#             project.title = request.form['project_title']
#             project.description = request.form['project_description']
#             db.session.commit()
#             flash('Project updated successfully!', 'success')
#             return redirect(url_for('manage_projects'))
    
#         return render_template('edit_project.html', project=project)    

#     @app.route('/delete_project/<int:project_id>', methods=['POST'])
#     def delete_project(project_id):
#         project = Project.query.get_or_404(project_id)  # Fetch the project by ID
#         db.session.delete(project)  # Delete the project from the database
#         db.session.commit()  # Commit the changes to the database
#         flash('Project deleted successfully!', 'success')
#         return redirect(url_for('manage_projects'))
