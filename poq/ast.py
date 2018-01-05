import ply.lex as lex
import ply.yacc as yacc
import enum

try:
    from poq import parsetab
except ImportError:
    parsetab = None


class PoqDataType(enum.Enum):
    LIST = "list"
    DICT = "dict"
    UNDEF = "undefined"


class PoqParser(object):

    def __init__(self):
        self.lexer = None
        self.parser = None
        self._data = ()

    # List of token names.   This is always required
    tokens = (
        "IDENTITY",
        "OBJECT_INDEX",
        "ARRAY_ITERATOR",
        "ARRAY_INDEX",
        "ARRAY_SLICE"
    )

    # Regular expression rules for simple tokens
    t_IDENTITY = r"\."
    t_OBJECT_INDEX = r"\.[a-zA-Z_][a-zA-Z0-9_]*"
    t_ARRAY_ITERATOR = r"\[\]"
    t_ARRAY_INDEX = r"\[\d+\]"
    t_ARRAY_SLICE = r"\[\d*\:\d*\]"

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = '| \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # YACC
    def _get_data_part(self):
        return self._data[0]

    def _get_data_type(self):
        return self._data[1]

    def _set_data(self, data, data_type=None):
        if data_type is None:
            self._data = (data, self._get_data_type())
        else:
            self._data = (data, data_type)

    def _is_current_list(self):
        return self._data[1] == PoqDataType.LIST

    def _is_current_dict(self):
        return self._data[1] == PoqDataType.DICT

    def _is_none(self):
        return self._data[0] is None

    def p_filter_chain(self, p):
        """filter_chain : filter_chain filter
                        | filter"""
        if self._is_none():
            p[0] = None
        else:
            p[0] = self._get_data_part()
        self._set_data(p[0])

    def p_filter_identity(self, p):
        """filter : IDENTITY"""
        p[0] = self._get_data_part()

    def p_filter_object_index(self, p):
        """filter : OBJECT_INDEX"""
        if self._is_none():
            p[0] = None
        elif not self._is_current_list():
            # data is a dict, just get the value for the field
            field_name = p[1][1:]
            data_part = self._get_data_part()
            if field_name in data_part:
                p[0] = data_part[field_name]
            else:
                p[0] = None
            self._set_data(p[0])
        elif self._is_current_list():
            # data is a list, we need to iterator the list and get the value for each element
            field_name = p[1][1:]
            data_part = self._get_data_part()
            p[0] = list(map(lambda x: x.get(field_name, None), data_part))
            self._set_data(p[0])

    def p_filter_array_iterator(self, p):
        """filter : ARRAY_ITERATOR"""
        data_part = self._get_data_part()
        if not isinstance(data_part, list):
            raise TypeError("Expect LIST for filter: ", p)

        if not self._is_current_list():
            # if it's not a list type, then just change it to list:
            p[0] = data_part
            self._set_data(p[0], data_type=PoqDataType.LIST)
        else:
            # if it's already a list, we try to flatten it
            p[0] = [y for x in data_part for y in x]
            self._set_data(p[0])

    def p_filter_array_index(self, p):
        """filter : ARRAY_INDEX"""
        data_part = self._get_data_part()

        if not isinstance(data_part, list):
            raise TypeError("Expect LIST for filter: ", p)

        idx = int(str(p[1])[1:len(p[1])-1])

        if idx >= len(data_part):
            raise TypeError("Array index out of bound: ", p)
        p[0] = data_part[idx]
        self._set_data(p[0], data_type=PoqDataType.UNDEF)

    def p_filter_array_slice(self, p):
        """filter : ARRAY_SLICE"""
        data_part = self._get_data_part()
        if not isinstance(data_part, list):
            raise TypeError("Expect LIST for filter: ", p)

        parts = str(p[1]).split(":", maxsplit=2)
        idx_1 = parts[0][1:]
        idx_2 = parts[1][:len(parts[1])-1]

        p[0] = data_part[idx_1:idx_2]
        self._set_data(p[0], data_type=PoqDataType.LIST)

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    # Build the lexer
    def build(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self, tabmodule=parsetab, debug=False)

    def parse(self, data, script):
        if self.lexer is None:
            self.build()
        self._data = (data, PoqDataType.UNDEF)
        result = self.parser.parse(input=script)
        return result

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        return [token for token in self.lexer]
