#!/usr/bin/env python3
"""file to implement an authentication class"""

from flask import request
from models.user import User
from typing import List, TypeVar


class Auth:
    '''class to manage the API authentication'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''returns False, not required now'''
        return False

    def authorization_header(self, request=None) -> str:
        '''returns None'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''returns None'''
        return None
