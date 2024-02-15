#!/usr/bin/env python3
"""
Module for handling Session authentication routes
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False
)
def session_logout():
    """ Handle user logout """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
