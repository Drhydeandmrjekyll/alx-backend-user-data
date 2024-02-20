from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the provided email and password."""
        # Implementation of register_user method goes here...

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password are valid."""
        # Implementation of valid_login method goes here...

    def create_session(self, email: str) -> str:
        """Create session for the user corresponding to the provided email."""
        # Implementation of create_session method goes here...

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user corresponding to the provided session ID."""
        if session_id is None:
            return None
        return self._db.find_user_by(session_id=session_id)
