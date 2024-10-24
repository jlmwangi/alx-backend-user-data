#!/usr/bin/env python3
'''method to hash passwords'''

import bcrypt


def _hash_password(password: str) -> bytes:
    '''takes in a pw and returns a byte hashed version '''
    pwd = password.encode('utf-8')
    hashed_passwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed_passwd
