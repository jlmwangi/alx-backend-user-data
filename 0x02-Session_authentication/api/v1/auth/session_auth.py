#!/usr/bin/env python3
'''a class meant to authenticate sessions'''

from flask import request
from models.user import User
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
import binascii


class SessionAuth(Auth):
    '''a class that inherits from auth'''
    pass
