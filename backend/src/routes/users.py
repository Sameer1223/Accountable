from flask import Blueprint, jsonify, request, abort
from ..database.models import User
from ..auth.auth import requires_auth
import datetime

users_endpoints = Blueprint('users', __name__)

# ========================
# Users
# ========================

# For testing, lists all users
@users_endpoints.route('/users', methods=['GET'])
@requires_auth(permission='get:users')
def users(jwt):
    # Retrieve all users
    users = User.query.all()
    formatted_users = [user.long() for user in users]
    return jsonify({
        'success:': True,
        'users': formatted_users
        }), 200

# Get a specific user by id
@users_endpoints.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = User.query.filter(User.user_id==user_id).one_or_none()
        return jsonify({
            'success': True,
            'user': user.long()
            }), 200
    except:
        abort(422)

# Endpoint to get user by email, going to be used for login/inviting @TODO Incomplete
@users_endpoints.route('/users-by-email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    try:
        user = User.query.filter(User.email==email).one_or_none()
        return jsonify({
            'success': True,
            'user': user.long()
            }), 200
    except:
        abort(422)

# Add a user
@users_endpoints.route('/users', methods=['POST'])
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

# Update a user, used to update last checked day
@users_endpoints.route('/users/<string:user_id>', methods=['PATCH'])
def update_user(user_id):
    try:
        user = User.query.filter(User.user_id==user_id).one_or_none()

        if user == None:
            abort(404)

        # Update last login day
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