from .data_model import *


class Operation:
    def process(self, data: PoqData):
        pass


class FilterChain(Operation):
    def __init__(self, filters):
        self._filters = filters

    def append_filter(self, ft):
        self._filters.append(ft)
        return self

    def process(self, data: PoqData):
        v = data
        for ft in self._filters:
            v = ft.process(v)
        return v


class Identity(Operation):
    def process(self, data):
        return data


class DictIndex(Operation):
    def __init__(self, key):
        self._key = key

    def process(self, data: PoqData):
        if data.is_none():
            return data
        elif not data.is_list():
            if isinstance(data.get_data(), list):
                # if it's a list, we report error
                raise TypeError("Cannot index a list with string \"{}\"".format(self._key))

            # data is a dict, just get the value for the field
            return data.update_data(data.get_data().get(self._key, None))
        else:
            # data is a list, we need to iterator the list and get the value for each element
            return data.update_data(list(map(lambda x: x.get(self._key, None), data.get_data())))


class ListIterator(Operation):
    def process(self, data: PoqData):
        v = data.get_data()
        if not isinstance(v, list):
            raise TypeError("Expect LIST for filter: ", p)

        if not data.is_list():
            # if it's not a list type, then just change it to list:
            return data.update_data_type(PoqDataType.LIST)
        else:
            # if it's already a list, we try to flatten it
            return data.update_data([y for x in v for y in x])


class ListIndex(Operation):
    def __init__(self, idx):
        self._idx = idx

    def process(self, data: PoqData):
        v = data.get_data()
        if not isinstance(v, list):
            raise TypeError("Cannot index dict as list")

        if self._idx >= len(v):
            raise ValueError("Index out of bound: {}".format(self._idx))

        return data.update(v[self._idx], PoqDataType.UNDEF)


class ListSlice(Operation):
    def __init__(self, start_idx, end_idx):
        self._start = start_idx
        self._end = end_idx

    def process(self, data: PoqData):
        v = data.get_data()
        if not isinstance(v, list):
            raise TypeError("Cannot slice dict")

        start = int(self._start) if self._start is not None else 0
        end = int(self._end) if self._end is not None else len(v)

        return data.update(v[start:end], PoqDataType.LIST)


class BooleanOpEq(Operation):
    def __init__(self, filter_chain, value):
        self._filter_chain = filter_chain
        self._value = value

    def process(self, data: PoqData):
        v = self._filter_chain.process(data)
        return PoqData(v.get_data() == self._value, PoqDataType.BOOLEAN)


class Select(Operation):
    def __init__(self, bop):
        self._op = bop

    def process(self, data: PoqData):
        if not data.is_list():
            raise TypeError("Cannot select dict")

        v = list(filter(lambda x: self._op.process(PoqData(x, PoqDataType.UNDEF)).get_data(), data.get_data()))
        return data.update_data(v)
