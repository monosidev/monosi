from enum import Enum
from sys import stdout

class Color(Enum): # You may need to change color settings
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    ENDC = '\033[m'

class BaseFormatter:
    def __init__(self, output=stdout):
        self.output = output

    # def start(self, notification):
    #     self.start_sync_output()

    def write(self, text: str, color: Color):
        self.output.write(color.value)
        self.output.write(text)

    def stop(self, none_obj):
        pass
