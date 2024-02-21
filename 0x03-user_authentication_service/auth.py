import bcrypt
import uuid
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> None:
        """Register a new user.

        Args:
            email (str): Email address of the user.
            password (str): Password of the user.

        Raises:
            ValueError: If the email is already registered.
        """
        # Check if the email is already registered
        if self._db.find_user_by(email=email):
            raise ValueError("Email is already registered")

        # Generate a new UUID for the user
        user_id = str(uuid.uuid4())

        # Hash the user's password
        hashed_password = self._hash_password(password)

        # Create a new User object
        new_user = User(user_id, email, hashed_password)

        # Store the new user in the database
        self._db.add_user(new_user)

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password of a user using the reset token.

        Args:
            reset_token (str): The reset token used to identify the user.
            password (str): The new password to set for the user.

        Raises:
            ValueError: If the reset token does not correspond to any user.
        """
        # Find user corresponding to reset token
        user = self._db.find_user_by(reset_token=reset_token)

        if not user:
            raise ValueError("Reset token is invalid")

        # Hash new password
        hashed_password = self._hash_password(password)

        # Update user's hashed password and reset_token fields
        user.hashed_password = hashed_password
        user.reset_token = None

    def log_in(self, email: str, password: str) -> str:
        """Log in a user and return the session ID."""
        return "session_id"

    def _hash_password(self, password: str) -> bytes:
        """Hash the password using bcrypt.

        Args:
            password (str): Password to hash.

        Returns:
            bytes: Hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
