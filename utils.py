import hashlib
from datetime import datetime
from pytz import timezone


try:
    from simplecrypt import encrypt, decrypt
except ModuleNotFoundError as e:
    # On Windows platform could not install simplecrypt module, which creates
    # an issue for PyCharm
    pass

from base64 import urlsafe_b64encode, urlsafe_b64decode, b64encode, b64decode
from random import seed, randint

from pylib.exceptions import BasicException


################################################################################
# Exceptions
################################################################################
class HexDigestException(BasicException):
    def __init__(self, errmsg=''):
        super().__init__(errmsg)
        

################################################################################
# Classes
################################################################################
class Rotator():

    def __init__(self, sequence, forever=False, random_start=True):
        self.sequence = sequence
        self.forever = forever
        if random_start:
            self.index = randint(0, len(self.sequence)-1) if self.sequence else 0
        else:
            self.index = 0
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


################################################################################
# Functions
################################################################################

def boolify(arg):

    truth = ('y','Y','t','T','true','True','TRUE')

    if arg in truth:
        return True
    else:
        return False


def datetime_from_epoch(epoch, tz=None):
    tz = timezone('UTC') if not tz else timezone(tz)
    return datetime.fromtimestamp(epoch, tz)


def now():
    return int(datetime.now().timestamp())


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


def simple_decrypt64(key, cyphertext):
    try:
        return decrypt(key, urlsafe_b64decode(cyphertext)).decode('utf-8')
    except NameError as e:
        if 'decrypt' in e.args[0]:
            return urlsafe_b64decode(cyphertext.encode('utf-8')).decode('utf-8')
        raise e


def simple_encrypt64(key, cleartext):
    try:
        return urlsafe_b64encode(encrypt(key, cleartext)).decode('utf-8')
    except NameError as e:
        if 'encrypt' in e.args[0]:
            return urlsafe_b64encode(cleartext.encode('utf-8')).decode('utf-8')
        raise e


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

    
def test_encryption(key, cleartext):
    crypt = simple_encrypt64(key, cleartext)
    print(f'Crypt={crypt}')
    clear = simple_decrypt64(key, crypt)
    print(f'Clear={clear}')


def test_dt(epoch, tz=None):
    print(f'Timezone={tz}, Datetime={datetime_from_epoch(epoch, tz)}')


if __name__ == '__main__':
    test_hexdigest('This is test data')
    test_hexdigest('This is test data', 'secret')
    test_hexdigest(b'This is test data')
    test_hexdigest(b'This is test data', b'secret')
    test_hexdigest('This is test data', b'secret')
    test_hexdigest(b'This is test data', 1)
    test_hexdigest(5, b'secret')
    test_sequence_rotator()
    test_encryption('Key', 'This is a test message')
    test_dt(now())
    test_dt(now(), 'America/New_York')
    test_dt(now(), 'Asia/Jerusalem')
