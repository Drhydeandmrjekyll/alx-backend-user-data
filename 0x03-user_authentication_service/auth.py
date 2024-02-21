import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

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

    def _hash_password(self, password: str) -> bytes:
        """Hashes input password using bcrypt.

        Args:
            password (str): Password to hash.

        Returns:
            bytes: The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
