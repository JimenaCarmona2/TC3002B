cube = {
    'entero': {
        'entero': {
            '+':  'entero',
            '-':  'entero',
            '*':  'entero',
            '/':  'flotante',
            '>':  'entero',
            '<':  'entero',
            '!=': 'entero',
            '==': 'entero',
        },
        'flotante': {
            '+':  'flotante',
            '-':  'flotante',
            '*':  'flotante',
            '/':  'flotante',
            '>':  'entero',
            '<':  'entero',
            '!=': 'entero',
            '==': 'entero',
        },
    },
    'flotante': {
        'entero': {
            '+':  'flotante',
            '-':  'flotante',
            '*':  'flotante',
            '/':  'flotante',
            '>':  'entero',
            '<':  'entero',
            '!=': 'entero',
            '==': 'entero',
        },
        'flotante': {
            '+':  'flotante',
            '-':  'flotante',
            '*':  'flotante',
            '/':  'flotante',
            '>':  'entero',
            '<':  'entero',
            '!=': 'entero',
            '==': 'entero',
        },
    },
}

# Se verifica el tipo resultado de una operación y se usa para agregar a type_stack
def get_type_cube(left_type, right_type, op):
    return cube[left_type][right_type][op]