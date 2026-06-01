_BASES = {
    "global": {"entero": 1000, "flotante": 2000},
    "constante": {"entero": 3000, "flotante": 4000},
    "local": {"entero": 5000, "flotante": 6000},
    "temporal": {"entero": 7000, "flotante": 8000},
}

_SIZE = 1000  # slots por segmento

class MemoryManager:
    def __init__(self):
        # Contadores actuales por (scope, tipo) ej. (global, entero) -> 1000
        self._counters: dict[tuple, int] = {}
        # Tabla de constantes: valor -> dirección
        self._const_table: dict = {}
        self._reset_segment("global")
        self._reset_segment("constante")
        self._reset_segment("local")
        self._reset_segment("temporal")

    def _reset_segment(self, scope: str):
        for tipo, base in _BASES[scope].items():
            self._counters[(scope, tipo)] = base

    def _next(self, scope: str, tipo: str) -> int:
        key = (scope, tipo)
        if key not in self._counters:
            raise TypeError(f"Tipo {tipo} no existe en segmento {scope}")
        addr = self._counters[key]
        limit = _BASES[scope][tipo] + _SIZE
        if addr >= limit:
            raise MemoryError(
                f"Desbordamiento de memoria en segmento {scope}/{tipo} "
                f"(límite {limit})"
            )
        self._counters[key] += 1
        return addr

    def assign_global(self, tipo: str) -> int:
        return self._next("global", tipo)

    def assign_local(self, tipo: str) -> int:
        return self._next("local", tipo)

    def assign_temp(self, tipo: str) -> int:
        return self._next("temporal", tipo)

    # Si la constante ya se utilizó, se reutiliza la dirección
    def assign_const(self, value, tipo: str) -> int:
        if value in self._const_table:
            return self._const_table[value]
        addr = self._next("constante", tipo)
        self._const_table[value] = addr
        return addr

    # Resetea local y temporal en una nueva función
    def reset_local(self):
        self._reset_segment("local")
        self._reset_segment("temporal")
