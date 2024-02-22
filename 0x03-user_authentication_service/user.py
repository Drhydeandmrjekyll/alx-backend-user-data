#!/usr/bin/env python3
"""
Module for creating user database
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    """
    Creates/TRepresents table for users
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hash_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))


if __name__ == '__main__':
    print(User.__table__)

    for column in User.__table__.columns:
        print("{}: {}.".format(column, column.type))
