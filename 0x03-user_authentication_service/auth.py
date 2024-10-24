#!/usr/bin/env python3
'''method to hash passwords'''

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from user import User
from db import DB
import uuid


def _hash_password(password: str) -> bytes:
    '''takes in a pw and returns a byte hashed version '''
    pwd = password.encode('utf-8')
    hashed_passwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed_passwd


def _generate_uuid() -> str:
    '''return a string representation of a new uuid'''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''register a user and save to database'''
        db = self._db

        try:
            user = db.find_user_by(email=email)  # check for user presence
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hash_pwd = _hash_password(password)  # if not exists

            added_user = db.add_user(email, hash_pwd)

            return added_user

    def valid_login(self, email: str, password: str) -> bool:
        '''validate a users credentials'''
        db = self._db

        try:
            user = db.find_user_by(email=email)
            if user:
                if bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password):
                    return True
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        '''returns session id as a string'''
        db = self._db

        try:
            user = db.find_user_by(email=email)
            new_id = _generate_uuid()

            db.update_user(user.id, session_id=new_id)
            return new_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        '''find user from session_id'''
        db = self._db

        if session_id is None:
            return None

        try:
            user = db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(user_id: int) -> None:
        '''updates session id to none ie destroys a session'''
        db = self._db

        try:
            user = db.find_user_by(id=user_id)

            db.update_user(user.id, session_id=None)
            return None
        except NoResultFound:
            return None
