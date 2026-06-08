from typing import Any

_G_START, _G_END = 1000, 2999  # global   (entero 1000-1999, flotante 2000-2999)
_C_START, _C_END = 3000, 4999  # constante
_L_START, _L_END = 5000, 6999  # local
_T_START, _T_END = 7000, 8999  # temporal


class ExecutionMemory:
    """
    Memoria de ejecución en tiempo de corrida.

    Estructura:
        _global  : dict addr->valor  — variables globales (persistente durante toda la ejecución)
        _const   : dict addr->valor  — constantes (solo lectura, precargadas desde el compilador)
        _stack   : lista de frames   — un frame por llamada activa

    Cada frame es {'local': {addr: valor}, 'temp': {addr: valor}}.
    Las direcciones virtuales indexan directamente cada dict:
        addr - base  no es necesario; se usa addr como llave directa.

    Las mismas direcciones locales/temp (ej. 5000) pueden aparecer en múltiples frames
    porque cada función reutiliza el espacio virtual; el frame stack las distingue.
    """

    def __init__(self, const_table: dict):
        # const_table del compilador: (value, tipo) -> addr
        self._global: dict[int, object] = {}
        self._const: dict[int, object] = {
            addr: val for (val, _t), addr in const_table.items()
        }
        self._stack: list[dict] = []

    def push_frame(self, frame: dict | None = None):
        self._stack.append(frame or {"local": {}, "temp": {}})

    def pop_frame(self) -> dict:
        return self._stack.pop()

    def get(self, addr: int):
        if _G_START <= addr <= _G_END:
            return self._global.get(addr)
        if _C_START <= addr <= _C_END:
            return self._const[addr]
        if _L_START <= addr <= _L_END:
            return self._stack[-1]["local"].get(addr)
        if _T_START <= addr <= _T_END:
            return self._stack[-1]["temp"].get(addr)
        raise ValueError(f"Dirección virtual inválida: {addr}")

    def set(self, addr: int, value):
        if _G_START <= addr <= _G_END:
            self._global[addr] = value
        elif _L_START <= addr <= _L_END:
            self._stack[-1]["local"][addr] = value
        elif _T_START <= addr <= _T_END:
            self._stack[-1]["temp"][addr] = value
        else:
            raise ValueError(f"No se puede escribir en dirección {addr}")


class VirtualMachine:
    """
    Intérprete de cuádruplos para Patito.

    Opcodes soportados:
        Aritmética : +  -  *  /
        Relacional  : >  <  !=  ==
        Asignación  : =
        Control     : GOTO  GOTOF
        Salida      : PRINT
        Funciones   : ERA  PARAM  GOSUB  RETURN  ENDFUNC  RETVAL
        Fin         : END
    """

    def __init__(self, quads: list, func_dir, const_table: dict):
        self.quads = quads
        self.func_dir = func_dir
        self.mem = ExecutionMemory(const_table)
        self.ip = 0  # instruction pointer
        self._call_stack: list[int] = []  # direcciones de retorno (ip tras GOSUB)
        self._pending_frames: list[dict] = (
            []
        )  # frames preparados por ERA, apilados en GOSUB
        self._return_val = (
            None  # registro de retorno (escrito por RETURN, leído por RETVAL)
        )

    def _resolve(self, val) -> Any:
        """Convierte dirección virtual → valor; deja pasar strings y None tal cual."""
        if isinstance(val, int):
            return self.mem.get(val)
        return val

    def run(self):
        # frame del cuerpo principal: guarda temps del main
        self.mem.push_frame()
        while self.ip < len(self.quads):
            q = self.quads[self.ip]
            op = q.op

            if op == "END":
                break

            elif op == "=":
                self.mem.set(q.res, self._resolve(q.left))
                self.ip += 1

            elif op in ("+", "-", "*", "/"):
                l, r = self._resolve(q.left), self._resolve(q.right)
                if op == "+":   result = l + r
                elif op == "-": result = l - r
                elif op == "*": result = l * r
                else:           result = l / r
                self.mem.set(q.res, result)
                self.ip += 1

            elif op in (">", "<", "!=", "=="):
                l, r = self._resolve(q.left), self._resolve(q.right)
                result = {">": l > r, "<": l < r, "!=": l != r, "==": l == r}[op]
                self.mem.set(q.res, int(result))  # entero: 1 verdadero, 0 falso
                self.ip += 1

            elif op == "GOTOF":
                cond = self._resolve(q.left)
                self.ip = q.res if not cond else self.ip + 1

            elif op == "GOTO":
                self.ip = q.res

            elif op == "PRINT":
                val = q.left
                if isinstance(val, str):
                    print(val.strip('"'))
                else:
                    print(self._resolve(val))
                self.ip += 1

            elif op == "ERA":
                # crea un frame vacío que PARAM llenará antes de que GOSUB lo active
                self._pending_frames.append({"local": {}, "temp": {}})
                self.ip += 1

            elif op == "PARAM":
                # copia el argumento al slot del parámetro dentro del frame pendiente
                val = self._resolve(q.left)
                self._pending_frames[-1]["local"][q.res] = val
                self.ip += 1

            elif op == "GOSUB":
                func_info = self.func_dir.get_function(q.left)
                self._call_stack.append(self.ip + 1)  # guarda dirección de retorno
                self.mem.push_frame(self._pending_frames.pop())
                self.ip = func_info["dir_cuadruplo"]

            elif op == "RETURN":
                if q.left is not None:
                    self._return_val = self._resolve(q.left)  # guarda valor de retorno
                self.mem.pop_frame()
                self.ip = self._call_stack.pop()

            elif op == "ENDFUNC":
                self.mem.pop_frame()
                self.ip = self._call_stack.pop()

            elif op == "RETVAL":
                # deposita el valor de retorno en el temporal del llamador
                self.mem.set(q.res, self._return_val)
                self.ip += 1

            else:
                raise RuntimeError(f"Opcode desconocido: '{op}' en quad {self.ip}")
