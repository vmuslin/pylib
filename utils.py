import hashlib

from pylib.exceptions import BasicException


Truth = ('y','Y','t','T','true','True','TRUE')


class HexDigestException(BasicException):
    def __init__(self, errmsg=''):
        super().__init__(errmsg)
        

def boolify(arg):
    if arg in Truth:
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


if __name__ == '__main__':
    test_hexdigest('This is test data')
    test_hexdigest('This is test data', 'secret')
    test_hexdigest(b'This is test data')
    test_hexdigest(b'This is test data', b'secret')
    test_hexdigest('This is test data', b'secret')
    test_hexdigest(b'This is test data', 1)
    test_hexdigest(5, b'secret')
