"""Test running the command line."""
import importlib


def test_main():
    """Just call the main routine."""
    proc = importlib.import_module("gcc.tree.gcc-tu-reader-json-process")
    proc.main_routine("introspector/projects/linux/tools/perf/builtin-trace.i.001t.json", debug=False)

if __name__ == '__main__':
    test_main()
