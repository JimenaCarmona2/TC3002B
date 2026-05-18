from lexer import lexer
from parser import parser

def run(src, label):
    try:
        result = parser.parse(src, lexer=lexer.clone())
        print(f"[OK]   {label}")
    except Exception as e:
        print(f"[FAIL] {label} → {e}")

def run_fail(src, label):
    try:
        result = parser.parse(src, lexer=lexer.clone())
        print(f"[FAIL] {label} → debió fallar pero aceptó")
    except Exception as e:
        print(f"[OK]   {label} → rechazado correctamente")

# 1. programa mínimo
run("""
programa minimo ;
inicio
  { }
fin
""", "programa mínimo")

# 2. declaración de una variable
run("""
programa test ;
vars
  x : entero ;
inicio
  { x = 5 ; }
fin
""", "una variable entera")

# 3. múltiples variables en la misma línea
run("""
programa test ;
vars
  x, y, z : entero ;
inicio
  { x = 1 ; }
fin
""", "múltiples ids en una declaración")

# 4. múltiples declaraciones de vars
run("""
programa test ;
vars
  x : entero ;
  f : flotante ;
inicio
  { x = 1 ; f = 3.14 ; }
fin
""", "múltiples declaraciones de vars")

# 5. asignación con expresión aritmética
run("""
programa test ;
vars
  x : entero ;
inicio
  { x = 2 + 3 * 4 ; }
fin
""", "expresión aritmética con precedencia")

# 6. asignación con paréntesis
run("""
programa test ;
vars
  x : entero ;
inicio
  { x = ( 2 + 3 ) * 4 ; }
fin
""", "expresión con paréntesis")

# 7. expresión relacional >
run("""
programa test ;
vars
  x : entero ;
inicio
  { si ( x > 0 ) { x = 1 ; } ; }
fin
""", "condición con >")

# 8. si sin sino
run("""
programa test ;
vars
  x : entero ;
inicio
  {
    x = 10 ;
    si ( x > 5 ) { escribe ( x ) ; } ;
  }
fin
""", "si sin sino")

# 9. si con sino
run("""
programa test ;
vars
  x : entero ;
inicio
  {
    x = 10 ;
    si ( x > 5 ) { x = 1 ; } sino { x = 0 ; } ;
  }
fin
""", "si con sino")

# 10. ciclo mientras
run("""
programa test ;
vars
  x : entero ;
inicio
  {
    x = 0 ;
    mientras ( x < 10 ) haz { x = x + 1 ; } ;
  }
fin
""", "ciclo mientras")

# 11. escribe con expresión
run("""
programa test ;
vars
  x : entero ;
inicio
  { escribe ( x + 1 ) ; }
fin
""", "escribe con expresión")

# 12. escribe con letrero
run("""
programa test ;
inicio
  { escribe ( "hola mundo" ) ; }
fin
""", "escribe con letrero")

# 13. escribe con múltiples argumentos
run("""
programa test ;
vars
  x : entero ;
inicio
  { escribe ( x , x + 1 ) ; }
fin
""", "escribe con múltiples args")

# 14. factor con signo negativo
run("""
programa test ;
vars
  x : entero ;
inicio
  { x = -5 ; }
fin
""", "factor negativo")

# 15. [ estatuto ] vacío
run("""
programa test ;
inicio
  { [ ] }
fin
""", "[ ] vacío")

# 16. [ estatuto ] con contenido
run("""
programa test ;
vars
  x : entero ;
inicio
  { [ x = 1 ; x = 2 ; ] }
fin
""", "[ estatutos ] con contenido")

# 17. función nula sin retorno
run("""
programa test ;
nula saluda ( nombre : entero ) {
  vars
    x : entero ;
  { escribe ( nombre ) ; }
} ;
inicio
  { saluda ( 1 ) ; }
fin
""", "función nula")

# 18. función con tipo de retorno
run("""
programa test ;
entero doble ( n : entero ) {
  vars
    r : entero ;
  { r = n + n ; }
} ;
inicio
  { doble ( 3 ) ; }
fin
""", "función con tipo entero")

# 19. múltiples funciones
run("""
programa test ;
nula f1 ( x : entero ) {
  { escribe ( x ) ; }
} ;
nula f2 ( y : flotante ) {
  { escribe ( y ) ; }
} ;
inicio
  { f1 ( 1 ) ; f2 ( 2.0 ) ; }
fin
""", "múltiples funciones")

# 20. llamada con múltiples argumentos
run("""
programa test ;
nula suma ( a : entero , b : entero ) {
  { escribe ( a + b ) ; }
} ;
inicio
  { suma ( 3 , 4 ) ; }
fin
""", "llamada con múltiples args")

# 21. expresiones relacionales todas
for op, label in [("!=", "!="), ("==", "=="), ("<", "<"), (">", ">")]:
    run(f"""
programa test ;
vars
  x : entero ;
inicio
  {{ si ( x {op} 0 ) {{ x = 1 ; }} ; }}
fin
""", f"operador relacional {label}")

# casos inválidos

# 22. falta fin
run_fail("""
programa test ;
inicio
  { }
""", "falta fin")

# 23. falta semicolon en asignación
run_fail("""
programa test ;
vars
  x : entero ;
inicio
  { x = 5 }
fin
""", "falta ; en asignación")

# 24. vars sin declaraciones
run_fail("""
programa test ;
vars
inicio
  { }
fin
""", "vars sin declaraciones")

# 25. llamada con coma al final
run_fail("""
programa test ;
nula f ( x : entero ) {
  { }
} ;
inicio
  { f ( 1 , ) ; }
fin
""", "llamada con coma al final")

# 26. token inválido
run_fail("""
programa test ;
inicio
  { @ }
fin
""", "token inválido @")
