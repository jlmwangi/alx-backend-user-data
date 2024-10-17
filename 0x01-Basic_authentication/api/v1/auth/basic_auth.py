#!/usr/bin/env python3
"""a class BasicAuth that inherits from auth"""

from api.v1.auth.auth import Auth
from flask import request
from models.user import User
from typing import List, TypeVar


class BasicAuth(Auth):
    '''class inheriting from auth'''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the base64 part of the authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        result = authorization_header.split(" ")
        return result[-1]
