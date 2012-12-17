# Set of regular expressions defining a lexer for JavaScript.

import ply.lex as lex

reserved = {
    'else':     'ELSE',
    'false':    'FALSE',
    'function': 'FUNCTION',
    'if':       'IF',
    'return':   'RETURN',
    'true':     'TRUE',
    'var':      'VAR',
}

tokens = [
    'ANDAND',       # &&
    'COMMA',        # ,
    'DIVIDE',       # /
    'EQUAL',        # =
    'EQUALEQUAL',   # ==
    'GE',           # >=
    'GT',           # >
    'IDENTIFIER',   # factorial
    'LBRACE',       # {
    'LE',           # <=
    'LPAREN',       # (
    'LT',           # <
    'MINUS',        # -
    'NOT',          # !
    'NUMBER',       # 124 5.678
    'OROR',         # ||
    'PLUS',         # +
    'RBRACE',       # }
    'RPAREN',       # )
    'SEMICOLON',    # ;
    'STRING',       # "this is a \"tricky\" string"
    'TIMES',        # *
] + reserved.values()

states = (
    ('comment', 'exclusive'),
)

t_ignore = ' \t\r\f\v' # whitespace

def t_eolcomment(token):
    r'//[^\n]*'
    pass

t_ANDAND =      r'&&'
t_COMMA  =      r','
t_DIVIDE =      r'/'
t_EQUALEQUAL =  r'=='
t_EQUAL  =      r'='
t_GE     =      r'>='
t_GT     =      r'>'
t_LBRACE =      r'\{'
t_LE     =      r'<='
t_LPAREN =      r'\('
t_LT     =      r'<'
t_MINUS  =      r'-'
t_NOT    =      r'!'
t_OROR   =      r'\|\|'
t_PLUS   =      r'\+'
t_RBRACE =      r'\}'
t_RPAREN =      r'\)'
t_SEMICOLON =   r';'
t_TIMES  =      r'\*'

def t_IDENTIFIER(t):
    r'[A-Za-z][A-Za-z_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_NUMBER(t):
    r'-?[0-9]+(?:\.[0-9]*)?'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'"(?:(?:\\.)*|[^"\\]*)*"'
    t.value = t.value[1:-1] # strip off quotes
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_error(t):
    print "JavaScript Lexer: Illegal character line %s: %s" % (t.lexer.lineno, t.value[0])
    t.lexer.skip(1)

# -----------------------------------------------------------------------------
#   'comment' state.
# -----------------------------------------------------------------------------
t_comment_ignore = ' \t\r\f\v'

def t_comment(t):
    r'\/\*'
    t.lexer.begin('comment')

def t_comment_end(t):
    r'\*\/'
    t.lexer.lineno += t.value.count('\n')
    t.lexer.begin('INITIAL')

def t_comment_error(t):
    t.lexer.skip(1)
# -----------------------------------------------------------------------------

# We have included two test cases to help you debug your lexer. You will
# probably want to write some of your own.

if __name__ == "__main__":
    lexer = lex.lex()

    def test_lexer(input_string):
        lexer.input(input_string)
        result = []
        while True:
            tok = lexer.token()
            if not tok: break
            result.append(tok.type)
        return result

    input1 = """ - !  && () * , / ; { || } + < <= = == > >= else false function
    if return true var """

    output1 = ['MINUS', 'NOT', 'ANDAND', 'LPAREN', 'RPAREN', 'TIMES', 'COMMA',
    'DIVIDE', 'SEMICOLON', 'LBRACE', 'OROR', 'RBRACE', 'PLUS', 'LT', 'LE',
    'EQUAL', 'EQUALEQUAL', 'GT', 'GE', 'ELSE', 'FALSE', 'FUNCTION', 'IF',
    'RETURN', 'TRUE', 'VAR']

    print test_lexer(input1) == output1

    input2 = """
    if // else mystery
    =/*=*/=
    true /* false
    */ return"""

    output2 = ['IF', 'EQUAL', 'EQUAL', 'TRUE', 'RETURN']

    print test_lexer(input2) == output2

    input3 = """
    if /* true // else
    */
    """
    output3 = ['IF']
    print test_lexer(input3) == output3

    def test_lexer(input_string):
        lexer.input(input_string)
        result = []
        while True:
            tok = lexer.token()
            if not tok: break
            result.append((tok.type, tok.value))
        return result

    input4 = 'some_identifier -12.34 "a \\"escape\\" b"'
    output4 = [('IDENTIFIER', 'some_identifier'), ('NUMBER', -12.34), ('STRING', 'a \\"escape\\" b')]
    print input4
    print test_lexer(input4)
    print test_lexer(input4) == output4

    input5 = '-12x34'
    output5 = [('NUMBER', -12.0), ('IDENTIFIER', 'x'), ('NUMBER', 34.0)]
    print input5
    print test_lexer(input5)
    print test_lexer(input5) == output5

