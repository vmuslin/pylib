# This file defines basic exceptions used throughout my code

class BasicException(Exception):

    def __init__(self, errmsg=''):
        self.errmsg = errmsg

    def __str__(self):
        return self.errmsg
        

class AbstractException(BasicException):
    def __init__(self, errmsg):
        super().__init__(errmsg)
