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

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        '''returns user email and pwd from b64 decoded value'''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        result = decoded_base64_authorization_header.split(':')
        return result[0], result[-1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''returns the user instance based on email and password'''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        #  search user based on email
        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]
        #  varify password
        if user and user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''overloads auth and retrieves user instance for a request'''
        #  get auth header using method from base class
        auth_header = self.authorization_header(request)
        #  extract auth header
        extracted_header = \
            self.extract_base64_authorization_header(auth_header)
        #  decode authorization header
        decoded_header = \
            self.decode_base64_authorization_header(extracted_header)
        #  extract user credentials from decoded string
        email, password = self.extract_user_credentials(decoded_header)
        #  return user instance
        curr_user = self.user_object_from_credentials(email, password)
        return curr_user
