import os
from sqlalchemy import Column, String, Integer, Boolean
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

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

    # Relationship
    tasks = db.relationship("Task", backref="group", lazy=True)

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
    group_id = Column(Integer, db.ForeignKey('Group.g_id'))
    
    # Relationship
    #group = db.relationship("Group", backref="tasks", lazy=True)

    # Short form representation
    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'complete': self.complete,
            'streaks': self.streaks
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
            'group_id': self.group_id
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

