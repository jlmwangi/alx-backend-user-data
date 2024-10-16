#!/usr/bin/env python3
"""file to implement an authentication class"""

from flask import request
from models.user import User
from typing import List, TypeVar


class Auth:
    '''class to manage the API authentication'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Define which routes dont need authentication'''
        if path is None:
            return True
        normalized_path = path.rstrip('/')  # remove trailing slashes
        excluded_path_list = [excluded_path.rstrip('/')
                              for excluded_path in excluded_paths]

        if normalized_path in excluded_path_list:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        '''returns None'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''returns None'''
        return None
