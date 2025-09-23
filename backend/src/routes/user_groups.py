from flask import Blueprint, jsonify, request, abort
from database.models import User, Group
from auth.auth import requires_auth


user_groups_endpoints = Blueprint('user_groups', __name__)

# ========================
# User groups
# ========================  

# Add a user to a group
@user_groups_endpoints.route('/users/<string:user_id>/groups/<int:group_id>', methods=['PATCH'])
@requires_auth(permission='patch:add-user-to-group')
def add_user_group(jwt, user_id, group_id):
    try:
        if group_id == 0:
            return
        
        user = User.query.filter(User.user_id==user_id).one_or_none()

        # Get user groups string
        past = ""
        if user.groups is not None and user.groups != '':
            past = user.groups + ","
        
        # Add new group id to the user
        user.groups = past + str(group_id)
        user.update()

        # Increment number of members in the group
        group = Group.query.filter(Group.g_id==group_id).one_or_none()
        group.number_of_members += 1
        group.update()

        return jsonify({
            'success': True,
            'user': user.long()
            }), 200
    except:
        abort(422)

# Delete a user from a group
@user_groups_endpoints.route('/users/<string:user_id>/groups/<int:group_id>', methods=['DELETE'])
@requires_auth(permission='delete:user-group')
def delete_user_group(jwt, user_id, group_id):
    try:
        user = User.query.filter(User.user_id==user_id).one_or_none()

        # Get their groups list and remove it
        groups = user.groups.split(',')
        groups.remove(str(group_id))
        user.groups = ','.join(groups)
        user.update()

        # Decrement number of members in the group
        group = Group.query.filter(Group.g_id==group_id).one_or_none()
        group.number_of_members -= 1
        group.update()

        return jsonify({
            'success': True,
            'user': user.long()
            }), 200
    except:
        abort(422)