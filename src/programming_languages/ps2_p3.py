# JavaScript: Comments & Keywords
#
# In this exercise you will write token definition rules for all of the
# tokens in our subset of JavaScript *except* IDENTIFIER, NUMBER and
# STRING. In addition, you will handle // end of line comments
# as well as /* delimited comments */.
#
# We will assume that JavaScript is case sensitive and that keywords like
# 'if' and 'true' must be written in lowercase. There are 26 possible
# tokens that you must handle. The 'tokens' variable below has been
# initialized below, listing each token's formal name (i.e., the value of
# token.type). In addition, each token has its associated textual string
# listed in a comment. For example, your lexer must convert && to a token
# with token.type 'ANDAND' (unless the && is found inside a comment).
#
# Hint 1: Use an exclusive state for /* comments */. You may want to define
# t_comment_ignore and t_comment_error as well.

import ply.lex as lex

def test_lexer(lexer,input_string):
  lexer.input(input_string)
  result = [ ]
  while True:
    tok = lexer.token()
    if not tok: break
    result = result + [tok.type]
  return result

tokens = (
        'ANDAND',       # &&
        'COMMA',        # ,
        'DIVIDE',       # /
        'ELSE',         # else
        'EQUAL',        # =
        'EQUALEQUAL',   # ==
        'FALSE',        # false
        'FUNCTION',     # function
        'GE',           # >=
        'GT',           # >
#       'IDENTIFIER',   #### Not used in this problem.
        'IF',           # if
        'LBRACE',       # {
        'LE',           # <=
        'LPAREN',       # (
        'LT',           # <
        'MINUS',        # -
        'NOT',          # !
#       'NUMBER',       #### Not used in this problem.
        'OROR',         # ||
        'PLUS',         # +
        'RBRACE',       # }
        'RETURN',       # return
        'RPAREN',       # )
        'SEMICOLON',    # ;
#       'STRING',       #### Not used in this problem.
        'TIMES',        # *
        'TRUE',         # true
        'VAR',          # var
)

states = (
    ('javascriptmultilinecomment', 'exclusive'),
)

t_ignore = ' \t\r\f\v' # whitespace

reserved = {
    'else':     'ELSE',
    'false':    'FALSE',
    'function': 'FUNCTION',
    'if':       'IF',
    'return':   'RETURN',
    'true':     'TRUE',
    'var':      'VAR',
}

def t_eolcomment(token):
    r'//[^\n]*'
    pass

t_ANDAND =      r'&&'
t_COMMA  =      r','
t_DIVIDE =      r'/'
t_ELSE   =      r'else'
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

# -----------------------------------------------------------------------------
#   We are _not_ going to return an IDENTIFIER from here. Hence we expect
#   any matching string to be in the 'reserved' dictionary.
# -----------------------------------------------------------------------------
def t_IDENTIFIER(token):
    r'[a-z]+'
    token.type = reserved[token.value]
    return token
# -----------------------------------------------------------------------------

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_error(t):
    print "JavaScript Lexer: Illegal character line %s: %s" % (t.lexer.lineno, t.value[0])
    t.lexer.skip(1)

# -----------------------------------------------------------------------------
#   'javascriptmultilinecomment' state.
# -----------------------------------------------------------------------------
t_javascriptmultilinecomment_ignore = ' \t\r\f\v'

def t_javascriptmultilinecomment(token):
    r'\/\*'
    token.lexer.begin('javascriptmultilinecomment')

def t_javascriptmultilinecomment_end(token):
    r'\*\/'
    token.lexer.lineno += token.value.count('\n')
    token.lexer.begin('INITIAL')

def t_javascriptmultilinecomment_error(token):
    token.lexer.skip(1)
# -----------------------------------------------------------------------------

# We have included two test cases to help you debug your lexer. You will
# probably want to write some of your own.

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

