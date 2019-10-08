"""Exception handling for EXPLIoT."""
from sys import exc_info


def sysexcinfo():
    """"Return the systems's exception."""
    return "{}:{}".format(exc_info()[0].__name__, exc_info()[1])
