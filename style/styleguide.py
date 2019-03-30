# basic style guide for classes
# all py files should be in CamelCase.py
from User import *

class CamelCase:
    #empty line
    def __init__(self, first_name):
        self._first_name = first_name
    #empty line
    # function description or decorator e.g. @property
    def lower_case_with_underscores (self, first_name):
        return self._first_name
