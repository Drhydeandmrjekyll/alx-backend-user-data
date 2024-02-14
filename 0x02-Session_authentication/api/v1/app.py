#!/usr/bin/env python3
"""
Route module for the API
"""
import sys
from os import getenv

from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from api.v1.views import app_views
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.before_request
def before_request():
    """ Method to handle before request """
    request.current_user = auth.current_user(request)

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if request.path not in excluded_paths:
        if not auth.require_auth(request.path, excluded_paths):
            return abort(404)
        if auth.authorization_header(request) is None:
            return abort(401)
        if request.current_user is None:
            return abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
