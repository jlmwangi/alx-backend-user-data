#!/usr/bin/env python3
"""a class BasicAuth that inherits from auth"""

from api.v1.auth.auth import Auth
from flask import request
from models.user import User
from typing import List, TypeVar


class BasicAuth(Auth):
    '''class inheriting from auth'''
    pass
