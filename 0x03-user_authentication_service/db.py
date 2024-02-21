"""DB module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from typing import List

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, user: User) -> None:
        """Add a new user to the database"""
        self._session.add(user)
        self._session.commit()

    def find_user_by(self, **kwargs):
        """Find users by the given keyword arguments."""
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            print("Not found")
            return None
        except MultipleResultsFound:
            print("Multiple users found for the given query")
            return None
        except InvalidRequestError:
            print("Invalid")
            raise InvalidRequestError("Invalid query arguments")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes based on user_id and keyword arguments"""
        user = self.find_user_by(id=user_id)

        # Check if all kwargs correspond to user attributes
        valid_attributes = set(User.__dict__.keys())
        for key in kwargs.keys():
            if key not in valid_attributes:
                raise ValueError(f"Invalid attribute '{key}'")

        # Update user attributes
        for key, value in kwargs.items():
            setattr(user, key, value)

        # Commit changes to database
        self._session.commit()
