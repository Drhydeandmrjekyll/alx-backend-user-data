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

    def add_user(self, email: str, hash_password: str) -> User:
        """

        """
        user = User(email=email, hash_password=hash_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """

        """
        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError()

        user = self._session.query(User).filter_by(**kwargs).first()

        if user:
            return user
        raise NoResultFound()


if __name__ == '__main__':
    my_db = DB()

    user = my_db.add_user("test@test.com", "PwdHashed")
    print(user.id)

    find_user = my_db.find_user_by(email="test@test.com")
    print(find_user.id)

    try:
        find_user = my_db.find_user_by(email="test2@test.com")
        print(find_user.id)
    except NoResultFound:
        print("Not found")

    try:
        find_user = my_db.find_user_by(no_email="test@test.com")
        print(find_use.id)
    except InvalidRequestError:
        print("Invalid")
