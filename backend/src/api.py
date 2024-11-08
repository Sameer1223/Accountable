import os
import datetime
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Task, Group, User
#from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

#with app.app_context():
#    db_drop_and_create_all()

# Endpoints

# GET /tasks
# GET /tasks-today
# POST /tasks
# PATCH /tasks/{id}
# DELETE /tasks/{id}

# ROUTES
@app.route('/hello')
def hello():
    return "hello world"


# ========================
# Users
# ========================
@app.route('/users', methods=['GET'])
def users():
    # Retrieve all users
    users = User.query.all()
    formatted_users = [user.long() for user in users]
    return jsonify({
        'success:': True,
        'users': formatted_users
        }), 200


@app.route('/users', methods=['POST'])
def insert_user():
    body = request.get_json()
    name = body.get('name')

    if not name:
        abort(400)
    
    try:
        user = User(name=name)
        user.insert()
        return jsonify({
            'success': True,
            'user': [user.long()]
        }), 200
    except:
        abort(422)

@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    try:
        user = User.query.filter(User.user_id==user_id).one_or_none()

        if user == None:
                abort(404)

        now = datetime.datetime.now()
        day_of_the_week = now.weekday()
        if user.last_checked != day_of_the_week:
            user.last_checked = day_of_the_week
            user.update()

        return jsonify({
            'success': True,
            'user': user.long()
            }), 200
    except:
        abort(422)

# ========================
# Tasks
# ========================
# Route for testing
@app.route('/tasks', methods=['GET'])
def tasks():
    # Retrieve all tasks
    tasks = Task.query.all()
    formatted_tasks = [task.long() for task in tasks]
    return jsonify({
        'success:': True,
        'tasks': formatted_tasks
        }), 200

# Route for testing
@app.route('/tasks/<int:id>', methods=['GET'])
def getTaskById(id):
    task = Task.query.filter(Task.id == id).one_or_none()
    return jsonify({
        'success': True,
        'task': task.long()
    }), 200

@app.route('/tasks-today/<int:user_id>', methods=['GET'])
def tasks_today(user_id):
    # Retrieve tasks schedule for today
    # Get todays day
    now = datetime.datetime.now()
    day_of_the_week = now.weekday()

    tasks = Task.query.filter(Task.user_id == user_id, Task.days.contains(day_of_the_week)).all()
    formatted_tasks = [task.short() for task in tasks]
    return jsonify({
        'success:': True,
        'tasks': formatted_tasks
        }), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    # Post a new task
    body = request.get_json()
    name = body.get('name')
    frequency = body.get('frequency', 1)
    days = body.get('days', '0123456')
    category = body.get('category', 'Daily')
    shared = body.get('shared', False)
    user_id = body.get('user_id')

    if not name or not user_id:
        abort(400)
    
    try:
        task = Task(
            name=name,
            complete=False,
            frequency=frequency,
            days=days,
            category=category,
            streaks=0,
            shared=shared,
            user_id=user_id
            )
        task.insert()
        return jsonify({
            'success': True,
            'tasks': [task.long()]
        }), 200
    except:
        abort(422)

# Resets streaks for incompleted tasks and 
# resets completion state of completed tasks
@app.route('/update-streaks/<int:user_id>', methods=['PATCH'])
def update_streaks(user_id):
    try:
        user = User.query.filter(User.user_id == user_id).one_or_none()
        
        if not user:
            abort(404)

        # Get todays day and update all previous days since last checked
        cur = datetime.datetime.now().weekday()
        lc = user.last_checked
        daysSince = cur - lc if cur >= lc else (7 - lc) + cur
        # For all past days get tasks
        for i in range(daysSince):
            day = (lc + i) % 7
            # Get all previous days tasks
            tasks = Task.query.filter(Task.user_id == user_id, Task.days.contains(str(day))).all()

            # For all tasks, if complete set to incomplete, if not set streaks to 0
            for task in tasks:
                if not task.complete:
                    task.streaks = 0
                else:
                    task.complete = False
                task.update()
        return jsonify({
            "success": True
        })
    except:
        abort(422)

@app.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    try:
        body = request.get_json()

        task = Task.query.filter(Task.id==id).one_or_none()
        if task == None:
                abort(404)

        task.name = body.get('name', task.name)
        task.complete = body.get('complete', task.complete)
        task.frequency = body.get('frequency', task.frequency)
        task.days = body.get('days', task.days)
        task.category = body.get('category', task.category)
        task.streaks = body.get('streaks', task.streaks)
        task.shared = body.get('shared', task.shared)

        task.update()
        return jsonify({
            'success': True,
            'tasks': task.long()
            }), 200
    except:
        abort(422)

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        task = Task.query.filter(Task.id==id).one_or_none()
        if task is None:
            abort(404)
        task.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except:
        abort(422)

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@Done implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@Done implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404

'''
@Done implement error handler for AuthError
    error handler should conform to general task above
'''
#@app.errorhandler(AuthError)
def authorization_error(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "authorization error"
    }), 403