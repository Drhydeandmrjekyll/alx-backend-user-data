#!/usr/bin/env python3
"""Authentication module for managing API authentication."""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to check if authentication is required for a path
        """
        if not path or not excluded_paths:
            return True
        if path.endswith('/'):
            path = path[:-1]  # Remove trailing slash if present
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                excluded_path = excluded_path[:-1]
            if path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method to get the authorization header
        """
        return None

    def current_user(self, request=None):
        """ Method to get the current user
        """
        return None
