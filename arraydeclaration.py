import ply.lex as lex
import ply.yacc as yacc

# List of token names. This is always required
tokens = [
    'ID',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'ASSIGN',
    'INT',
    'FLOAT',
    'STRING',
]

# Regular expression rules for simple tokens
t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_ASSIGN = r'='

# Include INT token definition for integers
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Include FLOAT token definition for floating-point numbers
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Include STRING token definition for strings
def t_STRING(t):
    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_start(p):
    '''start : array_declaration'''
    print('Valid array declaration')

def p_array_declaration(p):
    '''array_declaration : ID ASSIGN array_literal'''

def p_array_literal(p):
    '''array_literal : LBRACKET list_elements RBRACKET'''

def p_list_elements(p):
    '''list_elements : value
                     | value COMMA list_elements'''

def p_value(p):
    '''value : INT
             | FLOAT
             | STRING
             | empty_array
             | array_with_elements
             | another_array
             | nested_array'''

def p_empty_array(p):
    '''empty_array : LBRACKET RBRACKET'''

def p_array_with_elements(p):
    '''array_with_elements : LBRACKET values RBRACKET'''

def p_another_array(p):
    '''another_array : ID ASSIGN array_with_elements'''

def p_nested_array(p):
    '''nested_array : LBRACKET array_with_elements COMMA array_with_elements COMMA array_with_elements RBRACKET'''

def p_values(p):
    '''values : value
              | value COMMA values'''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error")

parser = yacc.yacc()

# Test it out
while True:
    try:
        s = input("Enter: ")
    except EOFError:
        break
    if not s:
        continue
    parser.parse(s)
