import ply.lex as lex
import ply.yacc as yacc
from .buildins import *

try:
    from src.poq import parsetab
except ImportError:
    parsetab = None


class PoqParser(object):

    def __init__(self):
        self.lexer = None
        self.parser = None
        self._data = ()

    # List of token names.   This is always required
    tokens = (
        "DOT",
        "L_BRACKET",
        "R_BRACKET",
        "L_PAREN",
        "R_PAREN",
        "COLON",
        "EQ",
        "NUMBER",
        "STRING_VALUE",
        "FIELD_NAME",
        "SELECT"
    )

    literals = ":"

    # Regular expression rules for simple tokens
    t_DOT = r"\."
    t_L_BRACKET = r"\["
    t_R_BRACKET = r"\]"
    t_L_PAREN = r"\("
    t_R_PAREN = r"\)"
    t_COLON = r"\:"
    t_EQ = r"=="
    t_SELECT = r"select"
    t_NUMBER = r"[1-9]\d*"
    t_STRING_VALUE = r"\"[^\"]*\""
    t_FIELD_NAME = r"\.[a-zA-Z][a-zA-Z0-9_]*"

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
    def p_filter_chain(self, p):
        """filter_chain : filter_chain filter
                        | filter"""
        if len(p) == 2:
            p[0] = FilterChain([p[1]])
        else:
            p[0] = p[1].append_filter(p[2])

    def p_filter_identity(self, p):
        """filter : DOT"""
        p[0] = Identity()

    def p_filter_object_index(self, p):
        """filter : FIELD_NAME"""
        p[0] = DictIndex(p[1][1:])

    def p_filter_array_iterator(self, p):
        """filter : L_BRACKET R_BRACKET"""
        p[0] = ListIterator()

    def p_filter_array_index(self, p):
        """filter : L_BRACKET NUMBER R_BRACKET"""
        p[0] = ListIndex(int(p[2]))

    def p_filter_array_slice(self, p):
        """filter : L_BRACKET NUMBER COLON NUMBER R_BRACKET
                  | L_BRACKET NUMBER COLON R_BRACKET
                  | L_BRACKET COLON NUMBER R_BRACKET"""
        if len(p) == 6:
            p[0] = ListSlice(int(p[2], int(p[4])))
        else:
            if p[3] == ":":
                p[0] = ListSlice(int(p[2]), None)
            else:
                p[0] = ListSlice(None, int(p[3]))

    def p_boolean_eq(self, p):
        """boolean_eq : filter_chain EQ NUMBER
                      | filter_chain EQ STRING_VALUE"""
        if p[3][0] == '"':
            p[0] = BooleanOpEq(p[1], p[3][1:-1])
        else:
            p[0] = BooleanOpEq(p[1], int(p[3]))

    def p_filter_select(self, p):
        """filter : SELECT L_PAREN boolean_eq R_PAREN"""
        p[0] = Select(p[3])

    def p_error(self, p):
        if p:
            print(p)
            raise SyntaxError("Syntax error at '%s'" % p.value)
        else:
            raise SyntaxError("Syntax error at EOF")

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
    def test_lexer(self, script):
        self.lexer.input(script)
        return [token for token in self.lexer]

    def test_yacc(self, script):
        result = self.parser.parse(input=script)
        return result
