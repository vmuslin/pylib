# Configuration class for parsing YAML and other configuration formats

# Generic Python modules
import os.path
import re
from pprint import pprint

# 3rd party modules
import yaml

# My modules
import pylib.exceptions as exceptions


class ConfigException(exceptions.BasicException):
    def __init__(self, errmsg):
        super().__init__(errmsg)


class YAMLException(ConfigException):
    def __init__(self, errmsg):
        super().__init__(errmsg)


# Various helper methods
class BaseConfig():


    def __init__(self):
        self.params = None


    def mkpath(self, path, sep=None):
        'Change path separator from "/" to the os-specific separator.'
        
        if not path:
            return path
        if path[0] == '/':
            return os.sep + os.path.join(*path.split('/'))
        else:
            return os.path.join(*path.split('/'))


class YAMLConfig(BaseConfig):


    def __init__(self, yaml_string=None, yaml_filename=None):
        super().__init__()
        self.yaml_string = yaml_string
        self.yaml_filename = yaml_filename
        self.yaml_parse()


    def yaml_parse(self):
        # If YAML is a string then parse it
        if self.yaml_string:
            self.params = yaml.load(self.yaml_string, Loader=yaml.FullLoader)

        # If YAML is a file, the read it and parse it
        elif self.yaml_filename:
            with open(self.yaml_filename, 'r') as file:
                self.params = yaml.load(file, Loader=yaml.FullLoader)



class YAMLConfigWithMacros(YAMLConfig):

    MacroPattern = '\$\[[^\]]+?\]'  # Patter for non-greedy match of '$[macro]'
    MacroRE = None
    DefinitionTag = 'DEFINE'
    

    def __init__(self, yaml_string=None, yaml_filename=None):
        super().__init__(yaml_string, yaml_filename)
        self.regexp = None
        self.macros = None
        self.process_macros()


    def process_macros(self):

        # Process the DEFINE section first to replace all macros

        # Get the macros dictionary
        try:
            expansion_rules = self.params[YAMLConfigWithMacros.DefinitionTag]

            # Build the regular expression for the macro match
            if not YAMLConfigWithMacros.MacroRE:
                YAMLConfigWithMacros.MacroRE = re.compile(YAMLConfigWithMacros.MacroPattern)

            self.regexp = YAMLConfigWithMacros.MacroRE
                
        # If there are no macros, then there is nothing ot do
        except KeyError:
            return


        def build_expansion_dictionary():

            self.macros = {}

            for rule in expansion_rules:

                # Make sure that it is a valid macro expansion rule.
                # A macro expension rule is a dictionary with a single entry in the form of:
                #   { 'MACRO_NAME' : 'EXPANSION_VALUE' }

                if type(rule) != dict or len(rule) != 1:
                    raise YAMLException('Error: Invalid macro definition ' + str(rule))

                macro, expansion = list(rule.items())[0]
                macro = str(macro)
                expansion = str(expansion)

                # Find all macros in the definition
                matches = self.regexp.findall(expansion)

                # If there are any macros to expand
                if matches:

                    # Try to replace them with the already defined macros expansion rules
                    for match in matches:
                        try:
                            replacement = self.macros[match]
                        except KeyError:
                            raise YAMLException('Error: forward reference to ' + match +
                                                ' in macro definition ' + str(rule))

                        expansion = expansion.replace(match, replacement)

                self.macros['$[' + macro + ']'] = expansion


        def expand_yaml_macros():

            if self.yaml_string:
                yaml_string = self.yaml_string
            else:
                yaml_string = yaml.dump(self.params)
        
            matches = self.regexp.findall(yaml_string)
            
            if matches:
                for macro in set(matches):
                    yaml_string = yaml_string.replace(macro, self.macros[macro])

                self.params = yaml.load(yaml_string, Loader=yaml.FullLoader)

        build_expansion_dictionary()
        expand_yaml_macros()


def test():
    pat = '\$\[[^\]]+?\]'
    regex = re.compile(pat)

    string = '$[PROTOCOL]://$[SERVER]:$[PORT]'
    print('String: ', string)

    dic = { 'PROTOCOL' : 'http', 'SERVER' : 'my.server.com', 'PORT' : 2727 }
    print('Dictionary:')
    pprint(dic)
    macros = regex.findall(string)
    print('Macros:')
    pprint(macros)
    for m in macros:
        key = m[2:-1]
        print('Found:', m, 'Substituting:', key, 'with', dic[key])
        string = string.replace(m, str(dic[key]))
        print('Result:', string)


if __name__ == '__main__':
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', required=False, help='Config file')
    args = vars(ap.parse_args())
    filename = args['file']
    if not filename:
        filename = 'config/config.yaml'

    try:
        yc = YAMLConfigWithMacros(yaml_filename=filename)
        y = yc.params
        pprint(y)
        pprint(y['www'])
        root = yc.mkpath(y['dirs']['root'])
        print('Root: ', root)
        fname = yc.mkpath(y['dirs']['mydir'])
        print('Rootify: ', fname, ' = ', os.path.join(root, fname))
    except YAMLException as e:
        print('Got YAML exception!', e)
        
