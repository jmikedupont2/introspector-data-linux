The user type report will show the things that are user defined types.
We will start with type declarations, and collect the types that are associated with them.
In our sample set, the type decl, field decl, modify expression, variable declaration all are associated with 
bool type, record type, real type, pointer type, integer type, and enum type.

We will first check plantuml/type_decl.puml and we see that type decls have more types, 

* array_type	
* boolean_type	
* complex_type	
* enumeral_type	
* function_type	
* integer_type	
* pointer_type	
* real_type	
* record_type	
* union_type	
* void_type	

The next step would be to check what are the translation units of those type decls. 
There is a "srcp" attribute that we can use. in the expanded_data.json.xz we find those. In jq we can find them. 

`jq -r '.nodes[]|select(._type=="type_decl")| ._id + "\t" + .type + "\t" + .srcp' linux_clean.json >> user_type_report/type_decls.csv`


`cut -d: -f1 user_type_report/type_decls.csv  | cut -f3 | sort | uniq -c | sort -n`

This gives us the report of types per file:

```
      1 atomic.h
      1 <built-in>
      1 clockid_t.h
      1 clock_t.h
      1 compress.h
      1 cpumap.h
      1 FILE.h
      1 __FILE.h
      1 helpline.h
      1 locale_t.h
      1 pthreadtypes-arch.h
      1 rwsem.h
      1 setjmp.h
      1 sig_atomic_t.h
      1 sigevent-consts.h
      1 sigset_t.h
      1 sigval_t.h
      1 ss_flags.h
      1 strbuf.h
      1 struct_iovec.h
      1 struct_itimerspec.h
      1 struct_sched_param.h
      1 struct_sigstack.h
      1 struct_timespec.h
      1 struct_timeval.h
      1 struct_tm.h
      1 timer_t.h
      1 time_t.h
      1 time-utils.h
      1 timex.h
      1 unistd.h
      1 units.h
      1 utsname.h
      1 xyarray.h
      2 __fpos64_t.h
      2 __fpos_t.h
      2 list.h
      2 map_symbol.h
      2 progress.h
      2 refcount.h
      2 ring_buffer.h
      2 session.h
      2 sigaction.h
      2 __sigset_t.h
      2 __sigval_t.h
      2 stack_t.h
      2 stat.h
      2 statx.h
      2 stdarg.h
      2 symbol_conf.h
      2 target.h
      2 trace-seq.h
      2 waitflags.h
      3 array.h
      3 bpf-event.h
      3 confname.h
      3 cpu-set.h
      3 cputopo.h
      3 fcntl-linux.h
      3 inttypes.h
      3 __locale_t.h
      3 __mbstate_t.h
      3 perf.h
      3 perf_regs.h
      3 posix_types_64.h
      3 rbtree.h
      3 signal.h
      3 stddef.h
      3 stdio.h
      3 util.h
      4 branch.h
      4 compiler.h
      4 counts.h
      4 data.h
      4 evlist.h
      4 map_groups.h
      4 mmap.h
      4 select.h
      4 sigevent_t.h
      4 stdint-intn.h
      4 stdint-uintn.h
      4 trace-event.h
      5 dirent.h
      5 ordered-events.h
      5 pmu.h
      5 struct_FILE.h
      6 aio.h
      6 cookie_io_functions_t.h
      6 fcntl.h
      7 env.h
      7 header.c
      7 header.h
      8 int-ll64.h
      8 machine.h
      8 siginfo-consts.h
      8 thread-shared-types.h
      9 tool.h
     10 sigcontext.h
     11 stdlib.h
     11 ucontext.h
     12 parse-events.h
     12 siginfo_t.h
     13 symbol.h
     14 regex.h
     16 evsel.h
     16 pthread.h
     17 dso.h
     18 libelf.h
     20 auxtrace.h
     20 stdint.h
     22 libbpf.h
     22 pthreadtypes.h
     26 gelf.h
     26 posix_types.h
     33 perf_event.h
     51 
     59 event-parse.h
     78 bpf.h
     83 event.h
    104 elf.h
    115 types.h
```

We will focus on the following types, and we searched for those named to find the possible files. 

```
     17 dso.h https://code.woboq.org/linux/linux/tools/perf/util/dso.h.html
     18 libelf.h https://code.woboq.org/linux/include/libelf.h.html
     20 auxtrace.h https://code.woboq.org/linux/linux/tools/perf/util/auxtrace.h.html 
     22 libbpf.h https://code.woboq.org/linux/linux/tools/lib/bpf/libbpf.h.html
     26 gelf.h https://code.woboq.org/linux/include/gelf.h.html
     33 perf_event.h https://code.woboq.org/linux/linux/include/linux/perf_event.h.html
     59 event-parse.h https://code.woboq.org/linux/linux/tools/lib/traceevent/event-parse.h.html
     78 bpf.h https://code.woboq.org/linux/linux/include/linux/bpf.h.html
     83 event.h https://code.woboq.org/linux/linux/tools/perf/util/event.h.html
    104 elf.h https://code.woboq.org/linux/linux/include/linux/elf.h.html
```

The event.h seems to be the largest file in the perf section of the code. perf_event is a union that seems to be very interesting from browsing that file quickly,
lets see what we can find out. 

So starting with that file, we want to see the type decls, follow the types that are declared, then we want to see the usages of those types.
What are the types that are parts of those types, so what are the subtypes, the type of fields, the types defined in those.
We can recurse over the types multiple times. Define it N times.
What types use what types?
What decls declare those used types?
What are the identifiers of those decls?
What are the file names of those users and used types? What file uses what file?

Lets start with a notebook so that we can do this step by step.
