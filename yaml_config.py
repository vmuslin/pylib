# Configuration class for parsing YAML and other configuration formats

# Generic Python modules
import os.path
import subprocess

from pprint import pprint

# 3rd party modules
import yaml

# My modules
import pylib.exceptions as exceptions
from pylib.paths import path
import pylib.config


################################################################################
# Exceptions
################################################################################

class YAMLException(config.ConfigException):
    def __init__(self, errmsg):
        super().__init__(errmsg)


n################################################################################
# YAML based configuration classes
################################################################################


class ConfigData(config.Config):
    def __init__(self, cmd_args=None, string=None, filename=None):
        super().__init(cmd_args=cmd_args)
        self.string = string
        self.filename = filename


class YAMLConfig(ConfigData):

    def __init__(self, cmd_args=None, string=None, filename=None):
        super().__init__(cmd_args, string, filename)


    def load(self):
        self._yaml_parse()
        return self
        

    def _yaml_parse(self):
        # If YAML is a string then parse it
        if self.string:
            self.cfg = yaml.load(self.string, Loader=yaml.FullLoader)

        # If YAML is a file, the read it and parse it
        elif self.filename:
            with path(self.filename).open('r') as file:
                self.cfg = yaml.load(file, Loader=yaml.FullLoader)



class YAMLConfigM4(YAMLConfig):

    MacroProcessor = 'm4'

    def __init__(self, cmd_args=None, string=None, filename=None, defines=None):
        super().__init__(cmd_args, string, filename)
        self.defines = defines


    def load(self):
        # If YAML is a string then parse it
        if self.string:
            super().load()
        # If YAML is a file, the pass it through M4 and parse it
        elif self.filename:
            self._parse_file()

        return self


    def _parse_file(self):
        # If YAML is a file, the pass it through a pre-processor and then parse it
        if not self.filename:
            return

        file = str(path(self.filename))
        if self.defines:
            cmd = f'{YAMLConfigM4.MacroProcessor} {self.defines} {file}'
        else:
            cmd = f'{YAMLConfigM4.MacroProcessor} {file}'

        self.string = subprocess.run(cmd,
                                     shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     check=True,
                                     universal_newlines=True).stdout

        self.cfg = yaml.load(self.string, Loader=yaml.FullLoader)
        

if __name__ == '__main__':
    filename = 'config/config.yaml'

    try:
        if not filename:
            raise YAMLException('No config file specified')

        cfg = YAMLConfigM4(filename=filename, defines='-D ENV=DEV').load().cfg
        pprint(cfg)
        exit(0)

    except YAMLException as e:
        print('Got YAML exception!', e)
        
