#!/usr/bin/env python3
"""Authentication module for managing API authentication."""

from flask import request
from typing import List, TypeVar


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
        """ Method to get  current user """
        return None
