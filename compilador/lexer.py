from ply import lex

reserved = {
    'entero': 'INT',
    'flotante': 'FLOAT',
    'vars': 'VARS',
    'mientras': 'WHILE',
    'haz': 'DO',
    'si': 'IF',
    'sino': 'ELSE',
    'nula': 'NULL',
    'inicio': 'START',
    'fin': 'END',
    'programa': 'PROGRAM',
    'escribe': 'WRITE'
}

tokens = [
    'ID',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'GREATER',
    'LESS',
    'NOTEQUAL',
    'EQUAL',
    'LBRACKET',
    'RBRACKET',
    'SEMICOLON',
    'COMMA',
    'COLON',
    'CTE_ENT',
    'CTE_FLOT',
    'STRING'
] + list(reserved.values())

# expresiones regulares

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_GREATER = r'>'
t_LESS = r'<'
t_NOTEQUAL = r'!='
t_EQUAL = r'=='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_COLON = r':'

def t_CTE_FLOT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_ENT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()

# if __name__ == "__main__":
#     with open("test_programa.txt", "r", encoding="utf-8") as f:
#         data = f.read()
#     lexer.input(data)
#     print("TOKENS:")
#     for tok in lexer:
#         print(f"{tok.type}: {tok.value}")
