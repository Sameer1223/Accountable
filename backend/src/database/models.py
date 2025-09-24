import os
from dotenv import load_dotenv
from sqlalchemy import Column, String, Integer, Boolean
from flask_sqlalchemy import SQLAlchemy
import json

# Sensitive information, @TODO: move to env variable or .env file
database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
#database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
database_path = os.getenv("DATABASE_URL")

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Group(db.Model):
    __tablename__ = "Group"
    # Autoincrementing, unique primary key
    g_id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    g_name = Column(String(80), nullable=False)
    number_of_members = Column(Integer(), default=0)
    owner = Column(String(80), nullable=False)

    # Relationship
    tasks = db.relationship("Task", backref="group", lazy=True)

    def long(self):
        return {
            'g_id': self.g_id,
            'g_name': self.g_name,
            'number_of_members': self.number_of_members,
            'owner': self.owner
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class User(db.Model):
    __tablename__ = 'User'
    
    user_id = Column(String(80), primary_key=True)
    email = Column(String(80), nullable=False)
    #auth_id = Column(String(80), nullable=False)
    name = Column(String(80), nullable=False)
    last_checked = Column(Integer)
    groups = Column(String(180))

    def long(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'last_checked': self.last_checked,
            'groups': self.groups
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Task(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80), nullable=False)
    complete = Column(Boolean, nullable=False, default=False)
    frequency = Column(Integer, nullable=False, default=1)
    days = Column(String(7), nullable=False, default="0123456")
    category = Column(String(80), default = "daily")
    streaks = Column(Integer, nullable=False, default=0)
    shared = Column(Boolean, nullable=False, default=False)
    user_id = Column(String(80), db.ForeignKey('User.user_id'))
    group_id = Column(Integer, db.ForeignKey('Group.g_id'))
    number_completed = Column(Integer, default=0)
    members_completion = Column(String(180))
    
    # Relationship
    #group = db.relationship("Group", backref="tasks", lazy=True)

    # Short form representation
    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'complete': self.complete,
            'streaks': self.streaks,
            'user_id': self.user_id,
            'number_completed': self.number_completed
        }

    # Long form representation?
    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'complete': self.complete,
            'frequency': self.frequency,
            'days': self.days,
            'category': self.category,
            'streaks': self.streaks,
            'shared': self.shared,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'number_completed': self.number_completed,
            'members_completion': self.members_completion
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())

