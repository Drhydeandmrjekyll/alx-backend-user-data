#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound

from user import Base, User


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self.engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memorized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self.engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly added User object.

        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by the specified criteria.

        Args:
            **kwargs: Variable keyword arguments representing the search criteria.
                  These arguments should correspond to attributes of the User class.

        Returns:
            User: The User object matching the search criteria.

        Raises:
            InvalidRequestError: If the provided search criteria do not correspond to valid attributes of the User class.

        """
        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError()

        user = self._session.query(User).filter_by(**kwargs).first()

        if user:
            return user
        raise NoResultFound()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user with the specified user ID using the provided attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Variable keyword arguments representing the attributes to update.
                  These arguments should correspond to attributes of the User class.

        Raises:
            ValueError: If any of the provided attributes are not valid attributes of the User class.

        """
        user_to_update = self.find_user_by(id=user_id)

        for attr, value in kwargs.items():
            if hasattr(User, attr):
                setattr(user_to_update, attr, value)
            else:
                raise ValueError()
        self._session.commit()


if __name__ == '__main__':
    my_db = DB()

    email = "test@test.com"
    hashed_password = "hashedPwd"

    user = my_db.add_user(email, hashed_password)
    print(user.id)

    try:
        my_db.update_user(user.id, hashed_password='NewPwd')
        print("Password updated")
    except ValueError:
        print("Error")
