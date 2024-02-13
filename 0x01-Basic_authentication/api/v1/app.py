#!/usr/bin/env python3
"""
Route module for the API
"""
import sys
from os import getenv

from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin

from api.v1.views import app_views

print(sys.path)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

from . import app

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
