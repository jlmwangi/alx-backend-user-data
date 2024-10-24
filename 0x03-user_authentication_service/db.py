#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Type

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
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
        '''adds and saves the user to the database'''
        #  create a new session
        session = self._session

        #  create a new user
        new_user = User(email=email, hashed_password=hashed_password)

        session.add(new_user)
        session.commit()

        user_id = new_user.id

        session.close()

        new_user.id = user_id

        return new_user
