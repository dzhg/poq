import enum


class PoqDataType(enum.Enum):
    LIST = "list"
    DICT = "dict"
    BOOLEAN = "boolean"
    UNDEF = "undefined"


class PoqData:
    def __init__(self, data, data_type):
        self._data = data
        self._type = data_type

    def is_none(self):
        return self._data is None

    def is_list(self):
        return self._type == PoqDataType.LIST

    def is_dict(self):
        return self._type == PoqDataType.DICT

    def get_data(self):
        return self._data

    def get_data_type(self):
        return self._type

    def set_data(self, data):
        self._data = data

    def set_data_type(self, data_type):
        self._type = data_type

    def update_data(self, data):
        self.set_data(data)
        return self

    def update_data_type(self, data_type):
        self.set_data_type(data_type)
        return self

    def update(self, data, data_type):
        self.set_data(data)
        self.set_data_type(data_type)
        return self
