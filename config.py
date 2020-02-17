# Configuration class for parsing YAML and other configuration formats

# Generic Python modules
import os.path

# My modules
import pylib.exceptions as exceptions
from pylib.paths import path


################################################################################
# Exceptions
################################################################################

class ConfigException(exceptions.BasicException):
    def __init__(self, errmsg):
        super().__init__(errmsg)


################################################################################
# Helper functions
################################################################################

def get_file_contents(filename, mode='r'):
    with path(filename).open(mode) as file:
        return file.read()

def get_html(spec):
    if ('.html' == spec[-5:].lower()) or ('.htm' == spec[-4:].lower()):
        return get_file_contents(spec)
    return spec


################################################################################
# Base Configuration Classes
################################################################################

class Config():

    def __init__(self):
        self.params = None
        self.cmd_args = None

    def load(self, cmd_args=None):
        self.cmd_args = cmd_args
        return self

    
    def refresh(self):
        self.load()
