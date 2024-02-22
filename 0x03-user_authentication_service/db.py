#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

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
