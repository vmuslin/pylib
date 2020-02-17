import sys
import os.path
import logging

from pprint import pprint


Severity = { 'CRITICAL' : 50,
             'ERROR' : 40,
             'WARNING' : 30,
             'INFO' : 20,
             'DEBUG' : 10 }


class Program():

    def __init__(self,
                 argv_parser=None,
                 replace_sys_argv=None, # Can be supplied to argv_parser instead of sys.argv, which is the default
                 config=None, # Configuration object
                 logformat='%(asctime)s [%(name)s %(levelname)s]: %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S'):
        self.replace_sys_argv = replace_sys_argv
        self.argv_parser = argv_parser
        self.config = config
        self.logformat = logformat
        self.datefmt = datefmt

        self.progname = argv_parser.prog # os.path.basename(sys.argv[0]).split('.')[0]

        self.args = None
        self.log = None


    def initialize(self):
        self.parse_argv()
        self.initialize_logging(filename=self.args.logfile,
                                level=self.args.severity,
                                format=self.logformat,
                                datefmt=self.datefmt)
        self.load_config()
        return self


    def initialize_logging(self,
                           filename=None,
                           level=Severity['WARNING'],
                           format='%(asctime)s [%(name)s %(levelname)s]: %(message)s',
                           datefmt='%Y-%m-%d %H:%M:%S'):
        if self.args:
            logging.basicConfig(filename=filename,
                                level=level,
                                format=format,
                                datefmt=datefmt)
            self.log = logging.getLogger(self.progname)
        

    def load_config(self):
        if self.config:
            self.config.load(cmd_args=self.args)


    def parse_argv(self):
        if self.argv_parser:
            self.args = self.argv_parser.parse_args(self.replace_sys_argv)


    def run(self):
        pass


if __name__ == '__main__':

    from pylib.args import ArgumentParser

    class TestArgumentParser(ArgumentParser):

        def __init__(self, description=None):
            super().__init__(description=description)

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


    from pylib.config import Config

    class TestConfig(Config):

        def load(self, cmd_args):
            self.params = { 'arg1' : 1, 'arg2' : 2 }
            return self


    class TestProg(Program):
        def run(self):
            self.log.info('Running program')
            pprint(self.args)


    parser = TestArgumentParser()
    prog = TestProg(argv_parser=parser, config=TestConfig())

    try:
        prog.run()
    except Exception as e:
        logging.exception('+--- Exception ------------------------------------------------------------')
