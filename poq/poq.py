from .processor import PoqProcessor

_processor = PoqProcessor()


def _query(path, o):
    """ query the object using path"""

    return _processor.process(o, path)
