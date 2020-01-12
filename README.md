# introspector-data-linux
Introspector data repo from the linux kernel

We use the other repo github.com/jmikedupont2/gcc_py_introspector.git to process the tu files and produce a json file.
This can be done one time, the resulting json needs to be processed and we do that here.

One problem is that when we update the other repo, we need to update this one to trigger a build.

So you need to output on char per 10 minutes on travis and also you can run out of memory, so flush out the buffers regularlly.
