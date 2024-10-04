from flask import jsonify, request, render_template, flash, redirect, url_for
from models import db, User, Project, Milestone, Task
from werkzeug.security import generate_password_hash, check_password_hash

def init_routes(app):
    # Home route (if needed, can still render HTML or redirect)
    @app.route('/')
    def home():
        return jsonify(message="Welcome to the API")

    # About route (if needed, can still render HTML or return JSON)
    @app.route('/about')
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

    # User registration endpoint
    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data['username']
        password = data['password']
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Registration successful! Please log in."}), 201

    # User login endpoint
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Logic to generate and return JWT can be added here
            return jsonify({"message": "Login successful!"}), 200
        
        return jsonify({"message": "Invalid username or password."}), 401

    # API for managing projects
    @app.route('/api/projects', methods=['GET', 'POST'])
    def manage_projects():
        if request.method == 'POST':
            data = request.get_json()
            project_title = data['project_title']
            project_description = data['project_description']
            user_id = 1  # Replace with the actual logged-in user's ID

            new_project = Project(title=project_title, description=project_description, user_id=user_id)
            db.session.add(new_project)
            db.session.commit()
            return jsonify({"message": "Project created successfully!"}), 201

        page = request.args.get('page', 1, type=int)
        projects = Project.query.paginate(page=page, per_page=8)
        return jsonify([project.to_dict() for project in projects.items]), 200  # Assuming to_dict() method exists

    # API for editing a project
    @app.route('/api/projects/<int:project_id>', methods=['PUT'])
    def edit_project(project_id):
        project = Project.query.get_or_404(project_id)

        data = request.get_json()
        project.title = data['project_title']
        project.description = data['project_description']
        db.session.commit()
        return jsonify({"message": "Project updated successfully!"}), 200

    # API for deleting a project
    @app.route('/api/projects/<int:project_id>', methods=['DELETE'])
    def delete_project(project_id):
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return jsonify({"message": "Project deleted successfully!"}), 200

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
