from semantic_cube import get_type_cube
from memory import MemoryManager


class Quadruple:
    def __init__(self, op, left, right, res):
        self.op = op
        self.left = left
        self.right = right
        self.res = res

    def __repr__(self):  # representacion en cadena para imprimir
        def f(v):
            return "_" if v is None else str(v)  # '_' es campo vacío (=, 2, _, a)

        return f"({f(self.op)}, {f(self.left)}, {f(self.right)}, {f(self.res)})"


class QuadrupleGenerator:
    def __init__(self, mem: MemoryManager):
        self.mem = mem
        self.reset()

    def reset(self):
        self.operand_stack = []
        self.type_stack = []
        self.operator_stack = []
        self.jump_stack = []
        self.quadruple_queue = []

    # Retorna la dirección virtual del temporal para usar directamente en cuádruplos
    def new_temporal(self, tipo: str = "entero") -> int:
        return self.mem.assign_temp(tipo)

    def add_quad(self, op, left, right, res):
        self.quadruple_queue.append(
            Quadruple(op, left, right, res)
        )  # al final de quadruple_queue

    def quadruple_count(self):  # se usa en jump_stack para gotof/goto/backpatch
        return len(self.quadruple_queue)

    # llamada en reduccion gramatical (termino o exp)
    def gen_quad_arithmetic(self):
        op = self.operator_stack.pop()
        right = self.operand_stack.pop()
        left = self.operand_stack.pop()
        right_type = self.type_stack.pop()
        left_type = self.type_stack.pop()

        res_type = get_type_cube(left_type, right_type, op)
        temp = self.new_temporal(res_type)

        self.add_quad(op, left, right, temp)
        self.operand_stack.append(temp)
        self.type_stack.append(res_type)

    def gen_quad_relational(
        self, op
    ):  # recibe operador porque los relacionales no se apilan en operator_stack
        right = self.operand_stack.pop()
        left = self.operand_stack.pop()
        right_type = self.type_stack.pop()
        left_type = self.type_stack.pop()

        res_type = get_type_cube(left_type, right_type, op)
        temp = self.new_temporal(res_type)

        self.add_quad(op, left, right, temp)
        self.operand_stack.append(temp)
        self.type_stack.append(res_type)

    def gotof(self):
        cond = self.operand_stack.pop()
        self.type_stack.pop()
        self.add_quad("GOTOF", cond, None, None)
        self.jump_stack.append(self.quadruple_count() - 1)

    def goto(self):
        self.add_quad("GOTO", None, None, None)
        self.jump_stack.append(self.quadruple_count() - 1)

    def backpatch(self, idx):
        self.quadruple_queue[idx].res = (
            self.quadruple_count()
        )  # llena el destino de gotof/goto con el índice actual

    def print_quad(self):
        print("=" * 54)
        print(f"  {'#':<5} {'OP':<8} {'IZQ':<12} {'DER':<12} {'RES':<10}")
        print("-" * 54)
        for i, q in enumerate(self.quadruple_queue):

            def f(v):
                return "_" if v is None else str(v)

            print(
                f"  [{i}]  {f(q.op):<8} {f(q.left):<12} {f(q.right):<12} {f(q.res):<10}"
            )
        print("=" * 54)
