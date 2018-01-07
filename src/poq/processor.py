from .data_model import *
from .ast import PoqParser


class PoqProcessor:
    def __init__(self):
        self._parser = PoqParser()

    def process(self, data, script):
        ops = self._parser.parse(data, script)
        result = ops.process(PoqData(data, PoqDataType.UNDEF))
        return result.get_data()
