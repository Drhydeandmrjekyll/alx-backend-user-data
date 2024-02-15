#!/usr/bin/env python3
"""Authentication module for managing API authentication."""

import os
from flask import request
from typing import List


class Auth:
    """ Auth class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to check if authentication is required for a path """
        if not path or not excluded_paths:
            return True
        if path.endswith('/'):
            path = path[:-1]

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*"):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method to get the authorization header """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None):
        """ Method to get current user """
        return None

    def session_cookie(self, request=None):
        """ Returns cookie value from request """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)


class SessionAuth(Auth):
    """ SessionAuth class """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create Session ID for user """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
