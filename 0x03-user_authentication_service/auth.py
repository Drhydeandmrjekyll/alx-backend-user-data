#!/usr/bin/env python3
"""
Module to hash_password and interact with auth_DB
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
import uuid

from user import User


def _hash_password(password: str) -> bytes:
    """
        Hashes a password using bcrypt
        password: Raw bunhashed password
        return: Hashed password as bytes.
    """
    encoded_pwd = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_pwd = bcrypt.hashpw(encoded_pwd, salt)

    return hashed_pwd


def _generate_uuid() -> str:
    """
    Generate a new UUID string representation.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self) -> None:
        """
        Initialize Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """

        """
        try:
            existing_user = self._db.find_user_by(email=email)

            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_pwd = _hash_password(password)

        new_usr = self._db.add_user(email=email,
                                    hashed_password=hashed_pwd.decode(
                                        "utf-8"))
        self._db
        return new_usr

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password.encode('utf-8')
            provided_password = password.encode('utf-8')

            if bcrypt.checkpw(provided_password, hashed_password):
                return True
        except NoResultFound:
            pass

        return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user and return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None  # Return None if user does not exist

        session_id = str(uuid.uuid4())  # Generate new UUID for session ID
        user.session_id = session_id  # Set session ID for user
        self._db.commit()  # Commit changes to database

        return session_id


if __name__ == '__main__':
    email = 'me@me.com'
    password = 'mySecuredPwd'

    auth = Auth()

    try:
        user = auth.register_user(email, password)
        print("successfully created a new user!")
    except ValueError as err:
        print("could not create a new user: {}".format(err))

    try:
        user = auth.register_user(email, password)
        print("successfully created a new user!")
    except ValueError as err:
        print("could not create a new user: {}".format(err))
