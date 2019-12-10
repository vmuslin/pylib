import hashlib

from random import seed, randint

from pylib.exceptions import BasicException


class Rotator():


    def __init__(self, sequence, forever=False):
        self.sequence = sequence
        self.forever = forever
        self.index = randint(0, len(self.sequence)-1) if self.sequence else 0
        self.start_index = self.index
        self.rotation_started = False


    def __iter__(self):
        return self


    def __next__(self):
        if not self.sequence:
            raise StopIteration
        if not self.forever and self.rotation_started and self.index == self.start_index:
            self.reset()
            raise StopIteration

        self.rotation_started = True
        item = self.sequence[self.index]
        self.index = (self.index + 1) % len(self.sequence)
        return item


    def reset(self, pushback=False):
        self.rotation_started = False
        if pushback:
            self.index = (self.index - 1) % len(self.sequence)
            self.start_index = self.index


class HexDigestException(BasicException):
    def __init__(self, errmsg=''):
        super().__init__(errmsg)
        

def boolify(arg):

    truth = ('y','Y','t','T','true','True','TRUE')

    if arg in truth:
        return True
    else:
        return False


def hexdigest(data, secret=None):

    if data:
        if type(data) == str:
            data = bytes(data, 'utf-8')
        if type(data) != bytes:
            raise HexDigestException('Attempting to hash data with an ' \
                                     'improper datatype, has to be bytes')

        if secret:
            if type(secret) == str:
                    secret = bytes(secret, 'utf-8')
            if type(secret) != bytes:
                raise HexDigestException('Attempting to hash secret with an ' \
                                         'improper datatype, has to be bytes')
                    
            data = data + secret

        h = hashlib.sha256()
        h.update(data)
        return h.hexdigest()

    else:
        return data


def test_hexdigest(data, secret=None):
    if secret:
        try:
            print('Hashing data:', data, ' and secret:', secret)
            print(hexdigest(data, secret))
        except HexDigestException as e:
            print(e)
    else:
        try:
            print('Hashing data:', data)
            print(hexdigest(data))
        except HexDigestException as e:
            print(e)


def test_sequence_rotator():

    l = Rotator([1, 2, 3, 4, 5])

    count = 0

    for i in l:
        print(i)
        if count == 2:
            break
        count += 1

    print('-' * 10)

    l.reset(True)

    for i in l: print(i)

    print('-' * 10)

    count = 0
    l = Rotator(['a', 'b', 'c', 'd'], forever=True)
    for i in l:
        print(i)
        if count == 20:
            break
        count += 1

    

if __name__ == '__main__':
    test_hexdigest('This is test data')
    test_hexdigest('This is test data', 'secret')
    test_hexdigest(b'This is test data')
    test_hexdigest(b'This is test data', b'secret')
    test_hexdigest('This is test data', b'secret')
    test_hexdigest(b'This is test data', 1)
    test_hexdigest(5, b'secret')
    test_sequence_rotator()
