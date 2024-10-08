from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def get_id(self):
        return self.id

    # Optional: A method to convert the user to a dictionary format
    def to_dict(self):
        return {"id": self.id, "username": self.username}
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'    

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Format datetime as string
            
        }

class Milestone(db.Model):
    __tablename__ = 'milestones'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    milestone_id = db.Column(db.Integer, db.ForeignKey('milestones.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('Not Started', 'In Progress', 'Completed'), default='Not Started')
    creative_note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    due_date = db.Column(db.Date)
