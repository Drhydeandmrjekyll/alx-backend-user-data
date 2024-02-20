import bcrypt
from db import DB
from user import User
import uuid


def _generate_uuid() -> str:
    """Generate a string representation of a new UUID.

    Returns:
        str: String representation of the generated UUID.
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """Hashes the input password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the provided email and password.

        Args:
            email (str): Email of user.
            password (str): Password of user.

        Returns:
            User: User object.

        Raises:
            ValueError: If a user with provided email already exists.
        """
        # Check if user with provided email already exists
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists")

        # Hash password
        hashed_password = _hash_password(password)

        # Create new user in database
        new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the login credentials are valid.

        Args:
            email (str): Email of user.
            password (str): Password of user.

        Returns:
            bool: True if login credentials are valid, False otherwise.
        """
        # Locate user by email
        user = self._db.find_user_by(email=email)
        if user:
            # Check password using bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        return False
