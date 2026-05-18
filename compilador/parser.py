import ply.yacc as yacc
from lexer import tokens
from symbol_table import FunctionDirectory

func_dir = FunctionDirectory()
current_func = None
global_func = None

# precedencia de operadores

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'GREATER', 'LESS', 'NOTEQUAL', 'EQUAL')
)

# reglas gramaticales

def p_program(p):
    'programa : PROGRAM ID SEMICOLON vars funcs START cuerpo END'
    global current_func, global_func
    current_func = p[2] 
    global_func = p[2]
    func_dir.add_function(p[2], 'nula')

def p_vars(p):
    '''vars : VARS id_list
            | empty'''
    
# de vars
def p_id_list(p):
    '''id_list : ID COMMA id_list
               | ID COLON tipo SEMICOLON id_list
               | ID COLON tipo SEMICOLON'''
    if len(p) == 5 or len(p) == 6: # solo cuando existe el tipo
        func_dir.add_variable(current_func, p[1], p[3])
    
def p_tipo(p):
    '''tipo : INT
            | FLOAT'''
    
def p_cuerpo(p):
    'cuerpo : LBRACE estatuto_list RBRACE'

# de cuerpo y estatuto
def p_estatuto_list(p):
    '''estatuto_list : estatuto estatuto_list
                     | empty'''
    
def p_funcs(p):
    '''funcs : NULL ID LPAREN id_type_list RPAREN LBRACE vars cuerpo RBRACE SEMICOLON funcs
                | tipo ID LPAREN id_type_list RPAREN LBRACE vars cuerpo RBRACE SEMICOLON funcs
                | empty'''
    global current_func # no crear una nueva, utilizar la global para mantener el estado de la función actual
    if len(p) > 2: # si no es empty
        func_dir.add_function(p[2], p[1])
        current_func = p[2]
    else: # si se acabaron las funciones regresa a global
        current_func = global_func


# de funcs
def p_id_type_list(p):
    '''id_type_list : ID COLON tipo COMMA id_type_list
                    | ID COLON tipo
                    | empty'''
    if len(p) > 2:
        func_dir.add_param(current_func, p[1], p[3])
    
def p_asigna(p):
    'asigna : ID ASSIGN expresion SEMICOLON'

def p_expresion(p):
    '''expresion : exp
                | exp GREATER exp
                | exp LESS exp
                | exp NOTEQUAL exp
                | exp EQUAL exp'''
    
def p_exp(p):
    '''exp : termino
        | termino PLUS exp
        | termino MINUS exp'''
    
def p_termino(p):
    '''termino : factor
            | factor TIMES termino
            | factor DIVIDE termino'''

def p_factor(p):
    '''factor : LPAREN expresion RPAREN
              | PLUS factor_list
              | MINUS factor_list
              | factor_list'''

# de factor
def p_factor_list(p):
    '''factor_list : ID
                  | cte
                  | llamada'''
    if isinstance(p[1], str): # si es un ID. isintance verifica el tipo de dato
        local = func_dir.get_function(current_func)['tabla_variables'] # busca primero en local
        global_vars = func_dir.get_function(global_func)['tabla_variables']
        if not local.exists(p[1]) and not global_vars.exists(p[1]):
            raise Exception(f"Error: {p[1]} no está declarada")
    
def p_cte(p):
    '''cte : CTE_ENT
            | CTE_FLOT'''
    
def p_llamada(p):
    '''llamada : ID LPAREN expresion_list RPAREN
                | ID LPAREN RPAREN'''
    if not func_dir.exists(p[1]):
        raise Exception(f"Error: {p[1]} no está declarada")

# de llamada
def p_expresion_list(p):
    '''expresion_list : expresion
                | expresion COMMA expresion_list'''
    
def p_ciclo(p):
    '''ciclo : WHILE LPAREN expresion RPAREN DO cuerpo SEMICOLON'''

def p_condicion(p):
    '''condicion : IF LPAREN expresion RPAREN cuerpo ELSE cuerpo SEMICOLON
                | IF LPAREN expresion RPAREN cuerpo SEMICOLON'''
    
def p_imprime(p):
    '''imprime : WRITE LPAREN imprime_list RPAREN SEMICOLON'''

# de imprime
def p_imprime_list(p):
    '''imprime_list : expresion
                    | STRING
                    | expresion COMMA imprime_list
                    | STRING COMMA imprime_list'''
    
def p_estatuto(p):
    '''estatuto : asigna
                | condicion
                | ciclo
                | llamada SEMICOLON
                | imprime
                | LBRACKET estatuto_list RBRACKET'''
    
def p_empty(p):
    'empty :'
    pass
    
parser = yacc.yacc()