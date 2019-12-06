import os.path
from pathlib import Path


def path(path):
    '''Take a Posix path definition and build a pathlib.Path object'''

    newpath = None

    parts = path.split('/')

    # If separator is the first character, restore it
    if path[0] == '/':
        parts[0] = '/' + parts[0]

    # If ~ is first, then expand it to be the user's home directory
    if parts[0] == '~':
        parts[0] = os.path.expanduser('~')

    # Build Path object
    for p in parts:
        if not newpath:
            if len(p) == 2 and p[1] == ':':
                p = p + '\\'
            newpath = Path(p)
        else:
            newpath = newpath / p

    return newpath
