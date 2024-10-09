#!/usr/bin/env python3
'''encrypt user passwords'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''returns a byte string which is hashed and salted'''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
