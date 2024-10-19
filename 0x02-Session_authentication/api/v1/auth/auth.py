#!/usr/bin/env python3
"""file to implement an authentication class"""

from flask import request
from models.user import User
from typing import List, TypeVar
import os


_my_session_id = os.getenv('SESSION_NAME')


class Auth:
    '''class to manage the API authentication'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Define which routes dont need authentication'''
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == "":
            return True
        normalized_path = path.rstrip('/')  # remove trailing slashes
        excluded_path_list = [excluded_path.rstrip('/')
                              for excluded_path in excluded_paths]

        if normalized_path in excluded_path_list:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        '''returns None'''
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        '''returns None'''
        return None

    def session_cookie(self, request=None):
        '''returns a cookie value from a request'''
        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
