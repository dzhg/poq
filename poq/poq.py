from .ast import PoqParser

_parser = PoqParser()


def _query(path, o):
    """ query the object using path"""

    return _parser.parse(o, path)
