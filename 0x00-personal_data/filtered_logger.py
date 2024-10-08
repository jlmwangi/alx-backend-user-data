#!/usr/bin/env python3
''' a function that returns log message'''


import re


def filter_datum(fields: list, redaction: str,
                 message: str, separator: str) -> str:
    '''returns the log message obfuscated'''
    for field in fields:
        pattern = r"({}=)([^{}]+)".format(field, separator)
        message = re.sub(pattern, r"\1" + redaction, message)
    return message
