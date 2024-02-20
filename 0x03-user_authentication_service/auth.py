from db import DB


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session ID for the corresponding user.

        Args:
            user_id (int): ID of the user whose session is to be destroyed.

        Returns:
            None
        """
        # Get user from the database using the user_id
        user = self._db.find_user_by_id(user_id)

        # Check if user exists
        if user:
            # Updates user'session ID to None
            self._db.update_user_session(user_id, None)
