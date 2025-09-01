from flask import Blueprint, jsonify, request, abort
from ..database.models import Group
from ..auth.auth import requires_auth

group_endpoints = Blueprint('groups', __name__)

# ========================
# Groups
# ========================

# For debugging, lists all groups
@group_endpoints.route('/groups', methods=['GET'])
@requires_auth(permission='get:groups')
def groups(jwt):
    # Retrieve all groups
    groups = Group.query.all()
    formatted_groups = [group.long() for group in groups]
    return jsonify({
        'success:': True,
        'groups': formatted_groups
        }), 200

# Get a specific group by id
@group_endpoints.route('/groups/<int:g_id>', methods=['GET'])
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

# Create a new group
@group_endpoints.route('/groups', methods=['POST'])
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