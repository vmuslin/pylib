# This class is deprecated

class YAMLConfigWithMacros(YAMLConfig):

    MacroPattern = '\$\[[^\]]+?\]'  # Patter for non-greedy match of '$[macro]'
    MacroRE = None
    DefinitionTag = 'DEFINE'
    DefaultPreprocessor = 'm4'
    

    def __init__(self, yaml_string=None, yaml_filename=None):

        super().__init__(yaml_string,yaml_filename)
        self.regexp = None
        self.macros = None


    def load(self):
        self._yaml_parse()
        self.process_macros()
        return self
        

    def process_macros(self):

        # Process the DEFINE section first to replace all macros

        # Get the macros dictionary
        try:
            expansion_rules = self.cfg[YAMLConfigWithMacros.DefinitionTag]

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

            if self.config_string:
                yaml_string = self.config_string
            else:
                yaml_string = yaml.dump(self.cfg)
        
            matches = self.regexp.findall(yaml_string)
            
            if matches:
                for macro in set(matches):
                    yaml_string = yaml_string.replace(macro, self.macros[macro])

                self.cfg = yaml.load(yaml_string, Loader=yaml.FullLoader)

        build_expansion_dictionary()
        expand_yaml_macros()


