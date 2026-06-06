import ply.yacc as yacc
from lexer import tokens
from symbol_table import FunctionDirectory
from quadruples import QuadrupleGenerator
from memory import MemoryManager

func_dir = FunctionDirectory()
mem = MemoryManager()
gen_quad = QuadrupleGenerator(mem)
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
    'programa : programa_header vars funcs START cuerpo END'
    gen_quad.print_quad()

def p_programa_header(p):
    'programa_header : PROGRAM ID SEMICOLON'
    global current_func, global_func
    func_dir.reset()
    gen_quad.reset()
    mem.__init__()          # resetea todos los segmentos al compilar de nuevo
    current_func = p[2]
    global_func = p[2]
    func_dir.add_function(p[2], 'nula')

# variables

def p_vars(p):
    '''vars : VARS id_list
            | empty'''
    
def p_id_list(p):
    '''id_list : ID COMMA id_list
               | ID COLON tipo SEMICOLON id_list
               | ID COLON tipo SEMICOLON'''
    # p[3] es el tipo explícito en "ID : tipo ;" o el tipo propagado desde id_list en "ID , id_list"
    tipo = p[3]
    if current_func == global_func:
        addr = mem.assign_global(tipo)
    else:
        addr = mem.assign_local(tipo)
    func_dir.add_variable(current_func, p[1], tipo, addr)
    # retorna tipo para que el nivel superior de la recursión lo lea como p[3] en "ID , id_list"
    p[0] = tipo

def p_tipo(p):
    '''tipo : INT
            | FLOAT'''
    p[0] = p[1]


# funciones

def p_funcs(p):
    '''funcs : funcs_nula_header LBRACE vars cuerpo RBRACE SEMICOLON funcs
             | funcs_tipo_header LBRACE vars cuerpo RBRACE SEMICOLON funcs
             | empty'''
    global current_func
    if len(p) > 2:
        current_func = global_func # regresa a global al salir

def p_funcs_nula_nombre(p):
    'funcs_nula_nombre : NULL ID'
    global current_func
    func_dir.add_function(p[2], 'nula')
    current_func = p[2]
    mem.reset_local()   # nuevo stack frame

def p_funcs_nula_header(p):
    'funcs_nula_header : funcs_nula_nombre LPAREN id_type_list RPAREN'

def p_funcs_tipo_nombre(p):
    'funcs_tipo_nombre : tipo ID'
    global current_func
    func_dir.add_function(p[2], p[1])
    current_func = p[2]
    mem.reset_local()   # nuevo stack frame

def p_funcs_tipo_header(p):
    'funcs_tipo_header : funcs_tipo_nombre LPAREN id_type_list RPAREN'

def p_id_type_list(p):
    '''id_type_list : ID COLON tipo COMMA id_type_list
                    | ID COLON tipo
                    | empty'''
    if len(p) > 2:
        addr = mem.assign_local(p[3])
        func_dir.add_param(current_func, p[1], p[3], addr)

# cuerpo y estatutos

def p_cuerpo(p):
    'cuerpo : LBRACE estatuto_list RBRACE'

def p_estatuto_list(p):
    '''estatuto_list : estatuto estatuto_list
                     | empty'''

def p_estatuto(p):
    '''estatuto : asigna
                | condicion
                | ciclo
                | llamada SEMICOLON
                | imprime
                | LBRACKET estatuto_list RBRACKET'''

# asignación

def p_asigna(p):
    'asigna : ID ASSIGN expresion SEMICOLON'
    res = gen_quad.operand_stack.pop()
    gen_quad.type_stack.pop()
    local_vars = func_dir.get_function(current_func)['tabla_variables']
    global_vars = func_dir.get_function(global_func)['tabla_variables']
    if local_vars.exists(p[1]):
        dest = local_vars.get_address(p[1])
    elif global_vars.exists(p[1]):
        dest = global_vars.get_address(p[1])
    else:
        raise Exception(f"Error semántico: '{p[1]}' no está declarada")
    gen_quad.add_quad('=', res, None, dest)

# expresión

def p_expresion(p):
    'expresion : exp'

def p_expresion_relacional(p):
    '''expresion : exp GREATER exp
                 | exp LESS exp
                 | exp NOTEQUAL exp
                 | exp EQUAL exp'''
    gen_quad.gen_quad_relational(p[2])

# exp

def p_exp(p):
    'exp : termino'

def p_exp_add(p):
    'exp : exp add_op termino'
    gen_quad.gen_quad_arithmetic()

def p_add_op(p):
    '''add_op : PLUS
              | MINUS'''
    gen_quad.operator_stack.append(p[1])

# termino

def p_termino(p):
    'termino : factor'

def p_termino_mult(p):
    'termino : termino mult_op factor'
    gen_quad.gen_quad_arithmetic()

def p_mult_op(p):
    '''mult_op : TIMES
               | DIVIDE'''
    gen_quad.operator_stack.append(p[1])

# factor

def p_factor_paren(p):
    'factor : LPAREN expresion RPAREN'

def p_factor_unary_plus(p):
    'factor : PLUS factor_list'

def p_factor_unary_minus(p):
    'factor : MINUS factor_list'
    operand = gen_quad.operand_stack.pop()
    tipo = gen_quad.type_stack.pop()
    temp = gen_quad.new_temporal(tipo)
    cero = 0 if tipo == 'entero' else 0.0
    gen_quad.add_quad('-', cero, operand, temp)
    gen_quad.operand_stack.append(temp)
    gen_quad.type_stack.append(tipo)

def p_factor_list(p):
    'factor : factor_list'

def p_factor_list_id(p):
    'factor_list : ID'
    local_vars = func_dir.get_function(current_func)['tabla_variables']
    global_vars = func_dir.get_function(global_func)['tabla_variables']
    if local_vars.exists(p[1]):
        tipo = local_vars.get_type(p[1])
        addr = local_vars.get_address(p[1])
    elif global_vars.exists(p[1]):
        tipo = global_vars.get_type(p[1])
        addr = global_vars.get_address(p[1])
    else:
        raise Exception(f"Error semántico: '{p[1]}' no está declarada")
    gen_quad.operand_stack.append(addr)
    gen_quad.type_stack.append(tipo)

def p_factor_list_cte_ent(p):
    'factor_list : CTE_ENT'
    addr = mem.assign_const(p[1], 'entero')
    gen_quad.operand_stack.append(addr)
    gen_quad.type_stack.append('entero')

def p_factor_list_cte_flot(p):
    'factor_list : CTE_FLOT'
    addr = mem.assign_const(p[1], 'flotante')
    gen_quad.operand_stack.append(addr)
    gen_quad.type_stack.append('flotante')

def p_factor_list_llamada(p):
    'factor_list : llamada'

# llamada

def p_llamada(p):
    '''llamada : ID LPAREN expresion_list RPAREN
                | ID LPAREN RPAREN'''
    func_name = p[1]
    if not func_dir.exists(func_name):
        raise Exception(f"Error semántico: función '{func_name}' no está declarada")
    func_info = func_dir.get_function(func_name)
    num_params = len(func_info['parametros'])
    for _ in range(num_params):
        if gen_quad.operand_stack:
            gen_quad.operand_stack.pop()
            gen_quad.type_stack.pop()
    gen_quad.add_quad('GOSUB', func_name, None, None)
    ret_type = func_info['tipo_retorno']
    if ret_type != 'nula':
        temp = gen_quad.new_temporal()
        gen_quad.add_quad('RETVAL', func_name, None, temp)
        gen_quad.operand_stack.append(temp)
        gen_quad.type_stack.append(ret_type)

def p_expresion_list(p):
    '''expresion_list : expresion
                      | expresion COMMA expresion_list'''

# imprime

def p_imprime(p):
    'imprime : WRITE LPAREN imprime_list RPAREN SEMICOLON'

def p_imprime_list(p):
    '''imprime_list : imprime_item
                    | imprime_list COMMA imprime_item'''

def p_imprime_item_expr(p):
    'imprime_item : expresion'
    val = gen_quad.operand_stack.pop()
    gen_quad.type_stack.pop()
    gen_quad.add_quad('PRINT', val, None, None)

def p_imprime_item_str(p):
    'imprime_item : STRING'
    gen_quad.add_quad('PRINT', p[1], None, None)

# condicion

def p_condicion_if_else(p):
    'condicion : IF LPAREN expresion RPAREN si_gotof cuerpo si_goto ELSE cuerpo si_fin SEMICOLON'

def p_condicion_if(p):
    'condicion : IF LPAREN expresion RPAREN si_gotof cuerpo si_fin_sin_else SEMICOLON'

def p_si_gotof(p):
    'si_gotof : empty'
    gen_quad.gotof()

def p_si_goto(p):
    'si_goto : empty'
    gen_quad.goto()
    false_jump = gen_quad.jump_stack[-2]
    gen_quad.jump_stack[-2] = gen_quad.jump_stack[-1]
    gen_quad.jump_stack.pop()
    gen_quad.backpatch(false_jump)

def p_si_fin(p):
    'si_fin : empty'
    end_jump = gen_quad.jump_stack.pop()
    gen_quad.backpatch(end_jump)

def p_si_fin_sin_else(p):
    'si_fin_sin_else : empty'
    false_jump = gen_quad.jump_stack.pop()
    gen_quad.backpatch(false_jump)

# ciclo

def p_ciclo(p):
    'ciclo : WHILE LPAREN while_inicio expresion RPAREN while_gotof DO cuerpo while_fin SEMICOLON'

def p_while_inicio(p):
    'while_inicio : empty'
    gen_quad.jump_stack.append(gen_quad.quadruple_count())

def p_while_gotof(p):
    'while_gotof : empty'
    gen_quad.gotof()

def p_while_fin(p):
    'while_fin : empty'
    false_jump = gen_quad.jump_stack.pop()
    start = gen_quad.jump_stack.pop()
    gen_quad.add_quad('GOTO', None, None, start)
    gen_quad.backpatch(false_jump)

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        raise Exception(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        raise Exception("Error de sintaxis: fin de archivo inesperado")

parser = yacc.yacc()