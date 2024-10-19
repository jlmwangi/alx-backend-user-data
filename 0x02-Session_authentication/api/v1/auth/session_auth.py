#!/usr/bin/env python3
'''a class meant to authenticate sessions'''

from flask import request
from models.user import User
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
import binascii
import uuid


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
