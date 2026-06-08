import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from lexer import lexer
from parser import parser, gen_quad, func_dir, mem
from virtual_machine import VirtualMachine

def run_file(path):
    label = os.path.basename(path)
    print(f"\n{'='*54}")
    print(f"  {label}")
    print('='*54)
    try:
        with open(path, encoding="utf-8") as f:
            src = f.read()
        parser.parse(src, lexer=lexer.clone())
        vm = VirtualMachine(gen_quad.quadruple_queue, func_dir, mem._const_table)
        vm.run()
    except Exception as e:
        print(f"[ERROR] {e}")

if len(sys.argv) > 1:
    for path in sys.argv[1:]:
        run_file(path)
else:
    tests_dir = os.path.join(os.path.dirname(__file__), "tests")
    for name in sorted(os.listdir(tests_dir)):
        if name.endswith(".txt"):
            run_file(os.path.join(tests_dir, name))
