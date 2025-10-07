from flask import Blueprint, jsonify, request, abort
from database.models import Task, User
from auth.auth import requires_auth
import datetime

tasks_endpoints = Blueprint('tasks', __name__)

# ========================
# Tasks
# ========================

# Route for testing, gets all tasks in the database @TODO (REMOVE LATER)
@tasks_endpoints.route('/tasks', methods=['GET'])
@requires_auth(permission='get:tasks')
def tasks(jwt):
    # Retrieve all tasks
    tasks = Task.query.all()
    formatted_tasks = [task.long() for task in tasks]
    return jsonify({
        'success:': True,
        'tasks': formatted_tasks
        }), 200

# Route for testing, gets a spefic task by id @TODO (REMOVE LATER)
@tasks_endpoints.route('/tasks/<int:id>', methods=['GET'])
def getTaskById(id):
    task = Task.query.filter(Task.id == id).one_or_none()
    if task is None:
        abort(404)
    return jsonify({ 
        'success': True, 
        'task': task.long() }), 200

# Get tasks scheduled for today for a specific user
# This is the endpoint a user will interact with the most
@tasks_endpoints.route('/tasks-today/<string:user_id>', methods=['GET'])
@requires_auth(permission='get:tasks-today')
def tasks_today(jwt, user_id):
    # Retrieve tasks schedule for today
    # Get todays day
    now = datetime.datetime.now()
    day_of_the_week = now.weekday()

    # Get group id, if 0 it indicates personal tasks in the individual tab
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

# Add/Create a new task
@tasks_endpoints.route('/tasks', methods=['POST'])
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

# Resets streaks for incompleted tasks and resets completion state of completed tasks
@tasks_endpoints.route('/update-streaks/<string:user_id>', methods=['PATCH'])
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

# Updates a task by id
@tasks_endpoints.route('/tasks/<int:id>', methods=['PATCH'])
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

# Deletes a task by id
@tasks_endpoints.route('/tasks/<int:id>', methods=['DELETE'])
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