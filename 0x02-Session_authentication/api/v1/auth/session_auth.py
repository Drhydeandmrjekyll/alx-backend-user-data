#!/usr/bin/env python3
"""Session authentication module for managing API authentication."""

import os
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth class for session-based authentication."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create session ID for a user."""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def current_user(self, request=None):
        """Get current user based on session."""
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        session_id = self.session_cookie(request)
        if session_id:
            return self.user_id_for_session_id(session_id)
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return User ID based on Session ID."""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
