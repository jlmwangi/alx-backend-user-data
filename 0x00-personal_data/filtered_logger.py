#!/usr/bin/env python3
''' a function that returns log message'''


import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    for field in fields:
        pattern = r"({}=)([^{}]+)".format(re.escape(field), re.escape(separator))
        message = re.sub(pattern, r"\1" + redaction, message)
    return message
