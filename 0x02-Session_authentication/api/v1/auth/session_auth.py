#!/usr/bin/env python3
'''a class meant to authenticate sessions'''

from flask import request
from models.user import User
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
import binascii
import uuid
import os


class SessionAuth(Auth):
    '''a class that inherits from auth'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a session id for a user_id'''
        if user_id is None or type(user_id) is not str:
            return None

        #  generate unique session id
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''returns a user id based on a session id'''
        if session_id is None or type(session_id) is not str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''returns a user instance based on a cookie value'''
        cookie_val = self.session_cookie(request)
        #  _my_session_id = os.getenv('SESSION_NAME')
        user_id = self.user_id_for_session_id(cookie_val)

        user = User.get(user_id)

        return user if user else None

    def destroy_session(self, request=None):
        '''delete user session/logout'''
        if request is None:
            return False

        session_id_cookie = self.session_cookie(request)
        if not session_id_cookie:
            return False

        session_user_id = self.user_id_for_session_id(session_id_cookie)
        if not session_user_id:
            return False

        # delete session from dict
        if session_id_cookie in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id_cookie]
            return True

        return False
