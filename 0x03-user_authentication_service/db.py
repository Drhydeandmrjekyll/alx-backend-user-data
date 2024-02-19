"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from typing import List

from user import Base, User

class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)  # Set echo to False
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> List[User]:
        """Find users by the given keyword arguments
        """
        try:
            users = self._session.query(User).filter_by(**kwargs).all()
            return users
        except NoResultFound:
            return []  # Return an empty list if no users are found
        except MultipleResultsFound:
            # Log a warning if multiple users are found
            print("Warning: Multiple users found for the given query")
            return []
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments")
