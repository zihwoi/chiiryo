from flask import jsonify, request, render_template, flash, redirect, url_for
from models import db, User, Project, Milestone, Task
from werkzeug.security import generate_password_hash, check_password_hash

def init_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/about')
    def about():
        fun_activities = [
            "creating interactive web applications.",
            "building fun games to play online.",
            "designing beautiful user interfaces.",
            "exploring new technologies and tools.",
            "collaborating with creative minds."
        ]
        return render_template('about.html', fun_activities=fun_activities)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']
            flash(f"Thank you, {name}! Your message has been sent.")
            return render_template('contact.html')
        return render_template('contact.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password)

            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                # Logic to generate and return JWT can be added here
                flash('Login successful!')
                return redirect(url_for('manage_projects'))  # Redirect to projects page

            flash('Invalid username or password.')

        return render_template('login.html')

    @app.route('/api/projects', methods=['GET', 'POST'])
    def manage_projects():
        if request.method == 'POST':
            project_title = request.form['project_title']
            project_description = request.form['project_description']
            user_id = 1  # Replace this with the actual logged-in user's ID

            new_project = Project(title=project_title, description=project_description, user_id=1)  # Replace 1 with the logged-in user's ID

            db.session.add(new_project)
            db.session.commit()
            
            flash('Project created successfully!')
            return redirect(url_for('manage_projects'))

        projects = Project.query.all()
        return render_template('projects.html', projects=projects)