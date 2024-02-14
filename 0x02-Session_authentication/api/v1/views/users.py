#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from api.v1.auth.basic_auth import BasicAuth


@app_views.route('/users/me', methods=['GET'], strict_slashes=False)
def get_authenticated_user() -> str:
    """ GET /api/v1/users/me
    Return:
      - Authenticated User object JSON represented
      - 404 if no authenticated user found
    """
    current_user = BasicAuth().current_user(request)
    if current_user is None:
        abort(404)
    return jsonify(current_user.to_json()), 200


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json()), 200

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON is the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create new User
    """
    rj = request.get_json()
    if not rj:
        return jsonify({'error': 'Invalid JSON'}), 400

    email = rj.get('email')
    password = rj.get('password')
    first_name = rj.get('first_name')
    last_name = rj.get('last_name')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        user = User()
        user.email = email
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
