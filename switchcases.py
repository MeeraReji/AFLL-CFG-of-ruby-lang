import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'CASE',
    'WHEN',
    'THEN',
    'ELSE',
    'END',
    'STRING',
    'VARIABLE',
    'PUTS',
    'GREATER',
    'LESS',
    'GREATEQ',
    'LESSEQ',
    'EQEQ',
    'NOTEQ',
    'INT'
)


t_ignore = ' \t\n'

def t_CASE(t):
    r'(\s)*case'
    return t
    
    
def t_WHEN(t):
    r'(\s)*when'
    return t
    
def t_THEN(t):
    r'(\s)*then'
    return t
    
def t_ELSE(t):
    r'(\s)*else'
    return t

def t_END(t):
    r'(\s)*end'
    return t
    
def t_PUTS(t):
    r'(\s)*puts'
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remove double quotes
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_GREATER(t):
    r'>'
    return t

def t_LESS(t):
    r'<'
    return t

def t_GREATEQ(t):
    r'>='
    return t

def t_LESSEQ(t):
    r'<='
    return t

def t_EQEQ(t):
    r'=='
    return t

def t_NOTEQ(t):
    r'!='
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

def p_case_statement(p):
    'case_statement : CASE VARIABLE case_when_list ELSE statements END'  
    p[0] = "Valid Ruby case-when statement"

def p_case_when_list(p):
    '''case_when_list : case_when
                      | case_when_list case_when'''
    pass

def p_case_when(p):
    'case_when : WHEN condition THEN statements'
    pass

def p_condition(p):
    '''condition : VARIABLE GREATER INT
                 | VARIABLE LESS INT
                 | VARIABLE GREATEQ INT
                 | VARIABLE LESSEQ INT
                 | VARIABLE EQEQ INT
                 | VARIABLE NOTEQ INT'''

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    pass

def p_statement(p):
    '''statement : PUTS STRING
                 | PUTS VARIABLE'''
                 

def p_error(p):
    if p:
         print(f"Syntax error at '{p.value}'")
    else:
         print(f"Invalid Syntax")

lexer = lex.lex()
parser = yacc.yacc()

def check_case_syntax(input_text):
    result = parser.parse(input_text)
    return result

input_text = """
case variable
when value > 5 then
  puts ""
when value < 5 then
  puts "Output 2"
else
  puts "Other output"
end
"""

result = check_case_syntax(input_text)
print(result)
