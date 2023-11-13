import ply.lex as lex
import ply.yacc as yacc

class Parser:
    tokens = ('BEGIN', 'RESCUE', 'ENSURE', 'END', 'STRING', 'COMMENT')

    t_BEGIN = r'\bbegin\b'
    t_RESCUE = r'\brescue\b'
    t_ENSURE = r'\bensure\b'
    t_END = r'\bend\b'
    t_STRING = r'"(?:\\.|[^"])*"'
    t_COMMENT = r'\#.*'

    t_ignore = ' \t'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character: {t.value[0]}")
        t.lexer.skip(1)

    def p_exception_handling(self, p):
        '''exception_handling : BEGIN statement_list rescue_clause optional_ensure END'''
        p[0] = True  # Syntax is valid

    def p_rescue_clause(self, p):
        '''rescue_clause : RESCUE statement_list'''
        p[0] = True  # Syntax is valid

    def p_optional_ensure(self, p):
        '''optional_ensure : ENSURE statement_list
                           | empty'''
        p[0] = True  # Syntax is valid

    def p_statement_list(self, p):
        '''statement_list : statement
                         | statement_list statement'''
        p[0] = True  # Syntax is valid

    def p_empty(self, p):
        'empty :'
        p[0] = True  # Syntax is valid

    def p_statement(self, p):
        '''statement : STRING
                     | COMMENT'''
        p[0] = True  # Syntax is valid

    def p_error(self, p):
        if not hasattr(self, 'error_reported') or not self.error_reported:
            yacc.error("Invalid syntax")
            self.error_reported = True

    def build_lexer(self):
        self.lexer = lex.lex(module=self)

    def build_parser(self):
        self.parser = yacc.yacc(module=self)

    def check_exception_handling(self, input_text):
        self.lexer.has_error = False
        self.error_reported = False  # Initialize error flag
        try:
            result = self.parser.parse(input_text, lexer=self.lexer)
            return result  # Will be True if syntax is valid
        except:
            return False  # Syntax is invalid

parser = Parser()
parser.build_lexer()
parser.build_parser()

input_text = """
begin
  # Code that might raise an exception
rescue
  # Handle the exception
ensure
  # Code that always runs, whether an exception occurred or not
end
"""

result = parser.check_exception_handling(input_text)
if result:
    print("Valid Syntax")
else:
    print("Invalid Syntax")