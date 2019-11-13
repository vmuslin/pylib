Truth = ('y','Y','t','T','true','True','TRUE')


def boolify(arg):
    if arg in Truth:
        return True
    else:
        return False


