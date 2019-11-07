# FileStreamReader

import inspect


class FileChangeObject():
    def __init__():
        pass
    def close(filename, nrows_in_file, nrows_in_stream):
        pass
    def open(filename, nrows_in_stream):
        pass

class NotFileChangeObject(Exception):
    pass


class FileStreamReader:

    def __init__(self, names, endtrim=None, file_change_object=None):
        self.names = names
        self.trim = endtrim
        self.nrows_in_file = 0
        self.nrows_in_stream = 0

        if file_change_object is not None and \
           not isinstance(file_change_object, FileChangeObject):
            raise NotFileChangeObject

        self.file_change_object = file_change_object

        self.len = len(names)
        self.index = 0
        # self.curfile is a reference to the currently open file object from the files.
        # specified in the list self.names. If the reference is None, then no object
        # current file is open and this is a new list.
        self.curfile = None


    # __enter__ method is used to implement the "with" statement
    def __enter__(self):
        return self


    # __exit__ method is used to implement the "with" statement
    def __exit__(self, type, value, traceback):
        self.close()


    # __iter__ method is used to implement interation over the FileStreamReader object
    def __iter__(self):
        return self


    # __iter__ method is used to implement interation over the FileStreamReader object
    def __next__(self):
        return self.readline()


    def __str__(self):
        return ''.join(('--- FileStreamReader  ---\n',
                        'Current file: ', str(self.filename), '\n',
                        str(self.names)))


    @property
    def filename(self):
        return self.names[self.index]


    def close(self):

        if self.curfile:
            self.curfile.close()
            self.curfile = None

        if self.index < self.len:
            if self.file_change_object is not None:
                self.file_change_object.close(self.filename, self.nrows_in_file, self.nrows_in_stream)
            self.index += 1
    

    def open_next(self):

        if self.index < self.len:
            self.curfile = open(self.filename)
            self.nrows_in_file = 0
            if self.file_change_object is not None:
                self.file_change_object.open(self.filename, self.nrows_in_stream)
            return True
        else:
            self.close()
            return False


    def readline(self):
        if self.curfile is None:
            if not self.open_next():
                raise StopIteration
        try:
            line = next(self.curfile)

            self.nrows_in_file += 1
            self.nrows_in_stream += 1
                                          
            if self.trim is not None:
                line = line[:self.trim]
        except StopIteration:
            self.close()
            if not self.open_next():
                raise StopIteration
            line = self.readline()

        return line


    @staticmethod
    def has_method(object, method):
        return hasattr(object, method) and inspect.ismethod(getattr(object, method))



#--- Tests ---

import glob
import sys

class FCO(FileChangeObject):
    def __init__(self):
        pass


    def close(self, filename, nrows_in_file, nrows_in_stream):
        print('Closing %s (%d/%d records)' % (filename, nrows_in_file, nrows_in_stream))
        

    def open(self, filename, nrows_in_stream):
        print('Opening %s (%d)' % (filename, nrows_in_stream))


def tests():

    fco = FCO()
    print('fco type is %s' % type(fco))


    if len(sys.argv) > 1:
        pattern = sys.argv[1]
    else:
        pattern = '*.py'

    print('pattern = %s' % pattern)
    files = glob.glob(pattern)
    print('files = %s' % files)
    
    try:
        with FileStreamReader(files, -1, fco) as fsr:
            for line in fsr:
                pass #print(line)

    except NotFileChangeObject as err:
        print('Error: not a FileChangeObject supplied')
    

if __name__ == '__main__':
    tests()
