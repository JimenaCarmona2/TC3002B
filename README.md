# Patito Compiler

A fully functional compiler for **Patito**, a small educational programming language with Spanish keywords. Built in Python using PLY (Python Lex-Yacc).

The compiler goes through all classical phases: lexical analysis → parsing → semantic analysis → intermediate code generation → execution on a custom virtual machine.

---

## Language Features

- Integer (`entero`) and float (`flotante`) types
- Global and local variable declarations (`vars`)
- Assignment, arithmetic (`+ - * /`), and relational operators (`> < != ==`)
- Conditional: `si` / `sino`
- Loop: `mientras … haz`
- Functions with parameters and return values (`regresa`)
- Print statement: `escribe`
- Recursive functions

### Example program

```
programa factorial_funcion;
vars
  r : entero;
entero factorial ( n : entero ) {
  vars
    resultado : entero;
  {
    resultado = 1;
    mientras ( n != 0 ) haz {
      resultado = resultado * n;
      n = n - 1;
    };
    regresa resultado;
  }
};
inicio
{
  r = factorial ( 5 );
  escribe ( "5! (funcion ciclica) =" );
  escribe ( r );
  si ( r > 100 ) {
    escribe ( "mayor a 100" );
  } sino {
    escribe ( "menor o igual a 100" );
  };
}
fin
```

---

## Architecture

```
Source (.txt)
     │
     ▼
  Lexer          lexer.py          Tokenizes keywords, identifiers, literals
     │
     ▼
  Parser         parser.py         LALR(1) grammar via PLY; drives all phases
     │
     ├──► Symbol Table   symbol_table.py   FunctionDirectory + VariableTable
     │
     ├──► Memory Manager  memory.py        Assigns virtual addresses per scope/type
     │
     ├──► Semantic Cube   semantic_cube.py  Type-checks every operation
     │
     └──► Quad Generator  quadruples.py    Produces flat quadruple list
               │
               ▼
     Virtual Machine    virtual_machine.py  Executes quadruples on segmented memory
```

### Virtual Address Scheme

| Segment    | `entero`    | `flotante`  |
|------------|-------------|-------------|
| Global     | 1000–1999   | 2000–2999   |
| Constant   | 3000–3999   | 4000–4999   |
| Local      | 5000–5999   | 6000–6999   |
| Temporal   | 7000–7999   | 8000–8999   |

### Quadruple Opcodes

`=` `+` `-` `*` `/` `>` `<` `!=` `==` `GOTO` `GOTOF` `WRITE`  
`ERA` `PARAM` `GOSUB` `RETURN` `ENDFUNC` `RETVAL` `END`

---

## Project Structure

```
compilador/
├── lexer.py            Tokenizer (PLY lex)
├── parser.py           Grammar rules + semantic actions (PLY yacc)
├── symbol_table.py     FunctionDirectory and VariableTable
├── memory.py           Virtual address allocator
├── semantic_cube.py    Type result table for all operator/type combinations
├── quadruples.py       Quadruple generator (stacks + backpatching)
├── virtual_machine.py  Stack-based VM with segmented memory
├── run.py              Entry point — runs all test files
└── tests/
    ├── test_factorial_ciclico.txt    Iterative factorial
    ├── test_factorial_funcion.txt    Function + while + si/sino
    └── test_fibonacci.txt            Doubly recursive Fibonacci
```

---

## How to Run

**Requirements:** Python 3.8+ and PLY

```bash
pip install ply
```

Run all tests:

```bash
cd compilador
python run.py
```

Run a single program:

```bash
python -c "
from parser import parser
with open('tests/test_factorial_ciclico.txt') as f:
    parser.parse(f.read())
"
```

---

## Test Cases

| File | What it tests | Output |
|------|---------------|--------|
| `test_factorial_ciclico.txt` | Variables, while loop, arithmetic | `120` |
| `test_factorial_funcion.txt` | Functions, parameters, while, si/sino, return | `120`, `mayor a 100` |
| `test_fibonacci.txt` | Double recursion, multiple simultaneous call frames | `55 89 144 233 377 610 987 1597` |

---

## Technologies

- **Python 3** — implementation language
- **PLY** — lexer and LALR(1) parser generator
