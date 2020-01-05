
cp -v ~/strings/linux_perf/*.tu ~/introspector-data-linux/
python3.7  -m  gcc.tree.gcc-tu-reader  ~/strings/linux_perf/*.tu  > builtin-trace.i.001t.json
