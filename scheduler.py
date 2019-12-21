import subprocess
import time
import argparse

from pylib.paths import path


REPEAT_FOREVER = 0
STDOUT = '__STDOUT__'


class Scheduler():

    def __init__(self,
                 interval=1,
                 repeat=REPEAT_FOREVER,
                 output=STDOUT):
        self.interval = interval
        self.repeat = repeat
        self.output = output


    def run(self, cmd):

        if self.output != STDOUT:
            with path(self.output).open('a') as file:
                self.run_loop(cmd, file)
        else:
            self.run_loop(cmd)


    def run_loop(self, cmd, file=None):
        while True:
            self.repeat -= 1
            output = self.run_command(cmd)
            if file:
                file.write(output)
                file.flush()
            if self.repeat == 0:
                break
            time.sleep(self.interval)


    def run_command(self, cmd):

        if self.output == STDOUT:
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


def scheduler():

    # Process command line arguments
    parser = argparse.ArgumentParser(description='Simmple Scheduler')
    parser.add_argument('-c', '--command',
                        required=True,
                        help='Shell command to run')
    parser.add_argument('-i', '--interval',
                        required=True,
                        default=1,
                        type=int,
                        help='Time to sleep between executions of the command')
    parser.add_argument('-o', '--output',
                        default=STDOUT,
                        help='Output file, if any')
    parser.add_argument('-r', '--repeat',
                        default=0,
                        type=int,
                        help='Specify how many times to repeat the command (default = unlimited)')

    args = parser.parse_args()

    # Launch scheduler

    s = Scheduler(interval=args.interval,
                  repeat=args.repeat,
                  output=args.output)

    s.run(args.command)
    

if __name__ == '__main__':

    try:
        scheduler()
    except Exception as e:
        print(e)
