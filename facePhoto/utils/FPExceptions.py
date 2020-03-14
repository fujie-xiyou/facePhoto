"""
Photo System Exceptions
"""


class FormException(Exception):
    def __init__(self, message, raw_exception=None):
        super().__init__(message)
        self.message = message
        self.raw_exception = raw_exception
