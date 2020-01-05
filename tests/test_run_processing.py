"Test running the command line."
import os


def test_main():
    print(os.system("python3 -m gcc.tree.gcc-tu-reader-json-process introspector/projects/linux/tools/perf/builtin-trace.i.001t.json"))
