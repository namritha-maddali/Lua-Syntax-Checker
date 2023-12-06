
import ply.lex as lex 
import ply.yacc as yacc 

tokens = (
    'FUNCTION', 
    'VARNAME', 
    'LPAREN', 
    'COMMA', 
    'RPAREN', 
    'IF',
    'ELSE',
    'STATEMENT',
    'REL_OPERATOR',
    'THEN',
    'NUMBER',
    'EQUAL',
    'IPAIRS',
    'PAIRS',
    'OR',
    'AND',
    'FOR',
    'DO',
    'IN',
    'STRING',
    'LCURLY',
    'RCURLY',
    'DOT',
    'NIL',
    'TABLE',
    'CREATE',
    'PCALL',
    'XPCALL',
    'END', 
)

t_LPAREN = r'\('
t_COMMA = r','
t_RPAREN = r'\)'
t_EQUAL = r'='
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_DOT = r"\."

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  
    return t

def t_STRING(t):
    r'(\'[^\']*\'|\"[^\"]*\")'
    return t

def t_VARNAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    reserved = {
        'function': 'FUNCTION', 'end': 'END', 
        'if': 'IF', 'else': 'ELSE', 'then': 'THEN', 
        'and': 'AND', 'or': 'OR', 
        'for': 'FOR', 'do': 'DO', 'ipairs': 'IPAIRS', 'pairs': 'PAIRS', 'in': 'IN',
        'nil': 'NIL', 'create':'CREATE', 'table':'TABLE', 'pcall':'PCALL', 'xpcall':'XPCALL'
    }
    t.type = reserved.get(t.value, 'VARNAME')
    return t

def t_STATEMENT(t):
    r'(?:function\s+[a-zA-Z_][a-zA-Z0-9_]*\(.*\)\s+end|if\s+.+\s+then\s+.+\s+end|while\s+.+\s+do\s+.+\s+end|for\s+[a-zA-Z_][a-zA-Z0-9_]*\s+=\s+.+\s+do\s+.+\s+end|repeat\s+.+\s+until\s+.+|local\s+[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.+|return\s+.+|break|print*\(.*\)|[\"\'][^\"\']*[\"\']|\b\w+\s*\(.*\)|\w+\s*(?:[\+\-\*/\%\^]|==|<=|>=|<>)?=.+|[a-zA-Z_][a-zA-Z0-9_]*)'
    return t

def t_REL_OPERATOR(t):
    r'(<=|>=|<|>|==|<>)'
    return t

t_ignore = ' \t\n'

# Error handling rule
def t_error(t):
    print(f"Syntax error at position {t.lexpos}, unexpected token '{t.value}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

flag = 0

def p_start(p):
    '''
    start : function
            | if
            | for
            | table
            | exception

    '''

def p_function(p):
    '''
    function : FUNCTION VARNAME LPAREN arguments RPAREN END 
             | FUNCTION VARNAME LPAREN RPAREN END
    '''

def p_arguments(p):
    '''
    arguments : VARNAME 
            | VARNAME COMMA arguments
    '''


def p_if(p):
    '''
    if : IF condition THEN statement else END
        | IF condition THEN statement if else END
        | IF condition THEN statement if else if END
        | IF condition THEN statement if END
        | IF condition THEN else END
        | IF condition THEN if END
        | IF condition THEN statement END
    '''

def p_else(p):
    '''
    else : ELSE statement
    '''

def p_condition(p):
    '''
    condition : condition logical_operator condition 
              | LPAREN condition logical_operator condition RPAREN
              | VARNAME REL_OPERATOR VARNAME
              | VARNAME REL_OPERATOR NUMBER
              | LPAREN VARNAME RPAREN
              | LPAREN VARNAME REL_OPERATOR VARNAME RPAREN
              | LPAREN VARNAME REL_OPERATOR NUMBER RPAREN
              | VARNAME
    '''

def p_logical_operator(p):
    '''
    logical_operator : AND
                      | OR
    '''


def p_for(p):
    '''
    for : FOR VARNAME methods DO statement END
    '''

def p_methods(p):
    '''
    methods : EQUAL variable COMMA variable COMMA variable
            | COMMA VARNAME IN VARNAME
            | COMMA VARNAME IN IPAIRS LPAREN VARNAME RPAREN
            | COMMA VARNAME IN PAIRS LPAREN VARNAME RPAREN
    '''


def p_statement(p):
    '''
    statement : STATEMENT
              | statement STATEMENT
              | if
              | function
              | for
              | function_call
    '''

def p_function_call(p):
    '''
    function_call : VARNAME LPAREN args RPAREN
    '''

def p_args(p):
    '''
    args : expression
         | expression COMMA args
         | LCURLY RCURLY
         | LCURLY list RCURLY
    '''

def p_expression(p):
    '''
    expression : VARNAME
               | NUMBER
               | STRING
               | function_call
               | key EQUAL value
               | NIL
    '''

def p_key(p):
    '''
        key : NUMBER
            | STRING
            | function_call
            | table
    '''

def p_value(p):
    '''
    value : key
          | NIL
    '''

def p_variable(p):
    '''
    variable : VARNAME
             | NUMBER 
    '''


def p_table(p):
    '''
    table : VARNAME EQUAL LCURLY RCURLY
          | VARNAME EQUAL LCURLY list RCURLY
          | VARNAME EQUAL TABLE DOT CREATE LPAREN variable COMMA expression RPAREN

    '''

def p_list(p):
    '''
    list : args
         | args COMMA list
    '''


def p_exception(p):
    '''
    exception : PCALL LPAREN VARNAME COMMA args RPAREN
              | XPCALL LPAREN VARNAME COMMA VARNAME COMMA args RPAREN
    '''


def p_error(p):
    print(f"Syntax error at position {p.lexpos}, unexpected token '{p.value}'")
    global flag
    flag = 1

# Build the parser
parser = yacc.yacc()

while True:
    # Get input from the user
    code_to_check = input("\nCode to check : ")

    # Check if the input is an empty string
    if not code_to_check.strip():
        print("\nExiting the parser.\n")
        break

    # Parse the user input
    parser.parse(code_to_check)
    if flag == 0:
        print("Valid Syntax")
    else:
        flag = 0

