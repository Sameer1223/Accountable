import os
import datetime
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from auth.auth import AuthError, requires_auth

from database.models import db_drop_and_create_all, setup_db, Task, Group, User


app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

with app.app_context():
    db_drop_and_create_all()

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
@requires_auth(permission='get:users')
def users(jwt):
    # Retrieve all users
    users = User.query.all()
    formatted_users = [user.long() for user in users]
    return jsonify({
        'success:': True,
        'users': formatted_users
        }), 200

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = User.query.filter(User.user_id==user_id).one_or_none()
        return jsonify({
            'success': True,
            'user': user.long()
            }), 200
    except:
        abort(422)

# Questionable route
@app.route('/users-by-email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    try:
        user = User.query.filter(User.email==email).one_or_none()
        return jsonify({
            'success': True,
            'user': user.long()
            }), 200
    except:
        abort(422)

@app.route('/users', methods=['POST'])
def insert_user():
    body = request.get_json()
    user_id = body.get('user_id')
    name = body.get('name')
    email = body.get('email')

    if not name:
        abort(400)
    
    user = User.query.filter(User.user_id == user_id).one_or_none()
    if user is not None:
        return jsonify({
            'user': [user.long()]
        }), 200
    
    try:
        user = User(user_id=user_id, name=name, email=email)
        user.insert()
        return jsonify({
            'success': True,
            'user': [user.long()]
        }), 200
    except:
        abort(422)

@app.route('/users/<string:user_id>', methods=['PATCH'])
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
# User groups
# ========================  

@app.route('/users/<string:user_id>/groups/<int:group_id>', methods=['PATCH'])
@requires_auth(permission='patch:add-user-to-group')
def add_user_group(jwt, user_id, group_id):
    try:
        if group_id == 0:
            return
        
        user = User.query.filter(User.user_id==user_id).one_or_none()

        past = ""
        if user.groups is not None and user.groups != '':
            past = user.groups + ","
        
        user.groups = past + str(group_id)
        user.update()

        group = Group.query.filter(Group.g_id==group_id).one_or_none()
        group.number_of_members += 1
        group.update()

        return jsonify({
            'success': True,
            'user': user.long()
            }), 200
    except:
        abort(422)

@app.route('/users/<string:user_id>/groups/<int:group_id>', methods=['DELETE'])
@requires_auth(permission='delete:user-group')
def delete_user_group(jwt, user_id, group_id):
    try:
        user = User.query.filter(User.user_id==user_id).one_or_none()

        groups = user.groups.split(',')
        groups.remove(str(group_id))
        user.groups = ','.join(groups)
        user.update()

        group = Group.query.filter(Group.g_id==group_id).one_or_none()
        group.number_of_members -= 1
        group.update()

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
@requires_auth(permission='get:tasks')
def tasks(jwt):
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

@app.route('/tasks-today/<string:user_id>', methods=['GET'])
@requires_auth(permission='get:tasks-today')
def tasks_today(jwt, user_id):
    # Retrieve tasks schedule for today
    # Get todays day
    now = datetime.datetime.now()
    day_of_the_week = now.weekday()

    group_id = request.args.get('group_id', '0')
    if group_id == '0':
        tasks = Task.query.filter(Task.user_id == user_id, Task.group_id==group_id, Task.days.contains(day_of_the_week)).all()
    else:
        tasks = Task.query.filter(Task.group_id == group_id, Task.days.contains(day_of_the_week)).all()

    formatted_tasks = [task.long() for task in tasks]
    return jsonify({
        'success:': True,
        'tasks': formatted_tasks
        }), 200

@app.route('/tasks', methods=['POST'])
@requires_auth(permission='post:tasks')
def create_task(jwt):
    # Post a new task
    body = request.get_json()
    name = body.get('name')
    frequency = body.get('frequency', 1)
    days = body.get('days', '0123456')
    category = body.get('category', 'Daily')
    shared = body.get('shared', False)
    user_id = body.get('user_id')
    group_id = body.get('group_id', 0)

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
            user_id=user_id,
            group_id=group_id
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
@app.route('/update-streaks/<string:user_id>', methods=['PATCH'])
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
@requires_auth(permission='patch:tasks')
def update_task(jwt, id):
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
        task.group_id = body.get('group_id', task.group_id)
        task.number_completed = body.get('number_completed', task.number_completed)
        task.members_completion = body.get('members_completion', task.members_completion)

        task.update()
        return jsonify({
            'success': True,
            'tasks': task.long()
            }), 200
    except:
        abort(422)

@app.route('/tasks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:tasks')
def delete_task(jwt, id):
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

# ========================
# Groups
# ========================
# For debugging
@app.route('/groups', methods=['GET'])
@requires_auth(permission='get:groups')
def groups(jwt):
    # Retrieve all groups
    groups = Group.query.all()
    formatted_groups = [group.long() for group in groups]
    return jsonify({
        'success:': True,
        'groups': formatted_groups
        }), 200

@app.route('/groups/<int:g_id>', methods=['GET'])
@requires_auth(permission='get:group-by-id')
def group_by_id(jwt, g_id):
    # Retrieve group by id
    print("GID:", g_id, flush=True)
    group = Group.query.filter(Group.g_id==g_id).one_or_none()
    if group is None:
        abort(404)
    return jsonify({
        'success:': True,
        'group': group.long()
        }), 200

@app.route('/groups', methods=['POST'])
@requires_auth(permission='post:groups')
def insert_group(jwt):
    body = request.get_json()
    name = body.get('name')
    owner = body.get('owner')
    if not name or not owner:
        abort(400)
    
    try:
        group = Group(g_name=name, owner=owner)
        group.insert()
        return jsonify({
            'success': True,
            'group': group.long()
        }), 200
    except:
        abort(422)

# ========================
# ERROR HANDLING
# ========================

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422



@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404


@app.errorhandler(AuthError)
def authorization_error(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "authorization error"
    }), 403