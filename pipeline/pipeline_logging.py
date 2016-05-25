import logging

class SuppressingFormatter(logging.Formatter):

    def formatException(self, exc_info):
        return ""

    def formatStack(self, stack_info):
        return ""
