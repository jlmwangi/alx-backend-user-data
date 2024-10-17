#!/usr/bin/env python3
"""a class BasicAuth that inherits from auth"""

from api.v1.auth.auth import Auth
from flask import request
from models.user import User
from typing import List, TypeVar
import base64
import binascii


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

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        '''returns the decoded value of a base64 string'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            '''check for validity'''
            decoded_bytes = base64.b64decode(base64_authorization_header)

            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string

        except (binascii.Error, UnicodeDecodeError):
            return None
