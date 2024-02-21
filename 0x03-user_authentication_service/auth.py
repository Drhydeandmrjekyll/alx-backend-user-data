import uuid
from db import DB


class Auth:
    def __init__(self):
        self._db = DB()

    def get_reset_password_token(self, email):
        """Generate a reset password token for user corresponding to the email.

        Args:
            email (str): Email of the user.

        Returns:
            str: Reset password token.

        Raises:
            ValueError: If no user is found with provided email.
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError(f"No user found with email: {email}")

        # Generate UUID for reset password token
        reset_token = str(uuid.uuid4())

        # Update user's reset_token database field
        self._db.update_user_reset_token(user.id, reset_token)

        return reset_token
