import argparse
import logging
import subprocess
import time

from pylib.paths import path
from pylib.program import Program
from pylib.args import ArgumentParser


REPEAT_FOREVER = 0
STDOUT = '__STDOUT__'
DEFAULT_INTERVAL_SECONDS = 1


class Scheduler(Program):

    def __init__(self, argv_parser=None):
        super().__init__(argv_parser=argv_parser)


    def run(self):
        try:
            self.log.info(f'Starting {self.progname}: running "{self.args.command}" every {self.args.repeat} seconds')
            if self.args.output != STDOUT:
                with path(self.args.output).open('a') as file:
                    self.run_loop(self.args.command,
                                  self.args.repeat,
                                  self.args.interval,
                                  file)
            else:
                self.run_loop(self.args.command,
                              self.args.repeat,
                              self.args.interval)
            
        except Exception as e:
            self.log.exception(f' {self.progname}')


    def run_loop(self, cmd, repeat, interval, file=None):
        while True:
            repeat -= 1
            output = self.run_command(cmd)
            if file:
                file.write(output)
                file.flush()
            if repeat == 0:
                break
            time.sleep(interval)


    def run_command(self, cmd):

        if self.args.output == STDOUT:
            subprocess.run(cmd,
                           shell=True,
                           check=True,
                           universal_newlines=True)
            return None
        else:
            return (subprocess.run(cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   check=True,
                                   universal_newlines=True).stdout)


class SchedulerArgumentParser(ArgumentParser):


    def __init__(self, description=None):
        super().__init__(description)


    def set_basic_args(self):
        self.add_argument('-c', '--command',
                          required=True,
                          help='Shell command to run')
        self.add_argument('-i', '--interval',
                          required=True,
                          default=DEFAULT_INTERVAL_SECONDS,
                          type=int,
                          help='Time to sleep between executions of the command')
        self.add_argument('-o', '--output',
                          default=STDOUT,
                          help='Output file, if any')
        self.add_argument('-r', '--repeat',
                          default=REPEAT_FOREVER,
                          type=int,
                          help='Specify how many times to repeat the command (default = unlimited)')
        self.add_argument('-s', '--severity',
                          default='WARNING',
                          choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                          help='Log level severity')
        self.add_argument('-l', '--logfile',
                          help='Name of the log output file')


if __name__ == '__main__':

    try:
        # Process command line arguments
        parser = SchedulerArgumentParser(description='Simmple Scheduler')

        # Launch scheduler
        s = Scheduler(argv_parser=parser)
        s.initialize()
        s.run()
    except Exception as e:
        raise e

