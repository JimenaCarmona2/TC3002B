class VariableTable:
    def __init__(self):
        self.variables = {}

    def add_variable(self, name, var_type, address: int):
        if name in self.variables:
            raise Exception(f"Error: {name} ya está declarada")
        self.variables[name] = {
            'tipo': var_type,
            'dir': address
        }

    def exists(self, name):
        return name in self.variables

    # Para verificar tipo de variable y agregarla en type_stack
    def get_type(self, name):
        if name not in self.variables:
            raise Exception(f"Error: {name} no está declarada")
        return self.variables[name]['tipo']

    def get_address(self, name) -> int:
        if name not in self.variables:
            raise Exception(f"Error: {name} no está declarada")
        return self.variables[name]['dir']

class FunctionDirectory:
    def __init__(self):
        self.functions = {}

    def add_function(self, name, return_type):
        if name in self.functions:
            raise Exception(f"Error: {name} ya está declarada")
        self.functions[name] = {
            'tipo_retorno': return_type,
            'parametros': [],
            'tabla_variables': VariableTable()
        }

    def add_param(self, func_name, param_name, param_type, address: int):
        self.functions[func_name]['parametros'].append({
            'nombre': param_name,
            'tipo': param_type,
            'dir': address,
        })
        self.functions[func_name]['tabla_variables'].add_variable(param_name, param_type, address)

    def add_variable(self, func_name, var_name, var_type, address: int):
        self.functions[func_name]['tabla_variables'].add_variable(var_name, var_type, address)

    def get_function(self, name):
        if name not in self.functions:
            raise Exception(f"Error: {name} no está declarada")
        return self.functions[name]

    def exists(self, name):
        return name in self.functions

    # Reinicia el directorio para tests
    def reset(self):
        self.functions = {}