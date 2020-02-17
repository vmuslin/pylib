import argparse
from pprint import pprint


class ArgNamespace(argparse.Namespace):

    def __init__(self, **kwargs):
        super().__init__(kwargs)


class ArgumentParser(argparse.ArgumentParser):


    def __init__(self, description=None):
        super().__init__(description=description)
        self.args = None
        self.set_basic_args()


    def set_basic_args(self):
        pass


    def parse_args(self, args=None, namespace=None):
        arguments = super().parse_args(args, namespace)
        return self.process_arguments(arguments)


    def process_arguments(self, arguments):
        return arguments


if __name__ == '__main__':

    class TestArgumentParser(ArgumentParser):
        def __init__(self, description=None):
            super().__init__(self)

        def set_basic_args(self):
            self.add_argument('-e', '--env',
                              required=True,
                              default='DEV',
                              choices=['DEV', 'TEST', 'PROD', 'WINDOWS'],
                              help='Name of the environment')
            self.add_argument('-d', '--dryrun',
                              action='store_true',
                              help='Flag indicating that this is a dry run')
            self.add_argument('-s', '--severity',
                              default='WARNING',
                              choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                              help='Log level severity')
            self.add_argument('-l', '--logfile',
                              help='Name of the log output file')

    parser = TestArgumentParser('Test of Program class')
    args = parser.parse_args()
    pprint(args)
        
