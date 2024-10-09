#!/usr/bin/env python3
''' a function that returns log message'''


import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector import Error


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
     """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''format method based on FORMAT'''
        original_msg = record.getMessage()
        record.msg = filter_datum(self.fields, self.REDACTION, original_msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''return unclear log message'''
    for field in fields:
        message = re.sub(r"({}=)([^{}]+)".format(re.escape(field),
                         re.escape(separator)), r"\1" + redaction, message)
    return message


def get_logger() -> logging.Logger:
    '''takes no arguments and returns a logging.Logger obj'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''returns a connector to the database'''
    user_name = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    pass_wd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host_name = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    connection = None
    connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=pass_wd,
            database=db_name
    )

    return connection


def main() -> None:
    '''obtains a db connection and retrieves all rows in users table'''
    db_conn = get_db()
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM users;')

    fields = PII_FIELDS
    log_record = get_logger()
    formatter = RedactingFormatter(fields)

    for row in cursor:
        formatted_record = formatter.format(row)
        log_record.info(formatted_record)

    cursor.close()
    db_conn.close()


if __name__ == "__main__":
    main()
