#!/usr/bin/env python3
'''encrypt user passwords'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''returns a byte string which is hashed and salted'''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''validates provided password'''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
