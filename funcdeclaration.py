import ply.lex as lex
import ply.yacc as yacc

class Parser:
    tokens = ('DEF','IDENTIFIER', 'LPAREN', 'RPAREN', 'STRING', 'PLUS', 'END', 'RETURN', 'PUTS', 'EQUALS', 'COMMA')

    t_PLUS = r'\+'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_EQUALS = r'='
    t_COMMA = r','

    t_ignore = ' \t'

    def t_DEF(self, t):
        r'\bdef\b'
        return t

    def t_END(self, t):
        r'\bend\b'
        return t

    def t_RETURN(self, t):
        r'\breturn\b'
        return t

    def t_PUTS(self, t):
        r'\bputs\b'
        return t

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        return t

    def t_STRING(self, t):
        r'"(?:\\.|[^"])*"'
        t.value = t.value[1:-1]
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character: {t.value[0]}")
        t.lexer.skip(1)

    def p_function_declaration(self, p):
        '''function_declaration : DEF IDENTIFIER LPAREN parameter_list RPAREN statement END'''
        p[0] = f"Function {p[2]} declared."

    def p_function_declaration_no_params(self, p):
        '''function_declaration : DEF IDENTIFIER statement END'''
        p[0] = f"Function {p[2]} declared."

    def p_parameter_list(self, p):
        '''parameter_list : parameter
                          | parameter COMMA parameter_list'''
        if len(p) > 2:
            p[0] = (p[1],) + p[3]
        else:
            p[0] = (p[1],)

    def p_parameter(self, p):
        '''parameter : IDENTIFIER
                     | IDENTIFIER EQUALS expression'''
        if len(p) > 1:
            if len(p) > 2:
                p[0] = (p[1], p[2], p[3])
            else:
                p[0] = p[1]

    def p_statement(self, p):
        '''statement : STRING PLUS expression
                     | STRING
                     | RETURN expression
                     | PUTS expression
                     | parameter_assignment
                     | empty'''
        if len(p) == 2 and p[1] is not None:
            p[0] = (p[1],)
        elif len(p) == 4:
            p[0] = (p[1], p[2], p[3])
        elif len(p) == 3:
            p[0] = (p[1], p[2])

    def p_parameter_assignment(self, p):
        '''parameter_assignment : IDENTIFIER EQUALS expression'''
        p[0] = (p[1], p[2], p[3])

    def p_empty(self, p):
        'empty :'
        p[0] = None

    def p_expression(self, p):
        '''expression : IDENTIFIER
                      | STRING
                      | expression PLUS expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2], p[3])

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Invalid syntax")

    def build_lexer(self):
        self.lexer = lex.lex(module=self)

    def build_parser(self):
        self.parser = yacc.yacc(module=self)

    def check_syntax(self, input_text):
        self.lexer.has_error = False
        result = self.parser.parse(input_text, lexer=self.lexer)
        if self.lexer.has_error:
            return "Function not declared due to lexer error"
        return result

parser = Parser()
parser.build_lexer()
parser.build_parser()

input_text = """
def greet3 (name="meera")
return "Hello, " + name
end
"""

result = parser.check_syntax(input_text)
print(result)
