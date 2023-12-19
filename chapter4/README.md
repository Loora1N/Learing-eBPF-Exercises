# Exercises for Chapter5 

这一章没什么实际题目，主要是一些工具使用，和一个简单代码改写([question5](./question5/mysolve.py))

另外，我将`starce -e bpf,perf_event_open,ioctl,ppoll ./hello-buffer-config.py`的syscall结果存入了[syscall.txt](syscall.txt)

## question5
Attaching to a raw tracepoint is considerably more straightforward at the syscall level than attaching to a kprobe, as it simply involves a `bpf()` syscall. Try converting **hello-buffer-config.py** to attach to the raw tracepoint for sys_enter, using BCC's `RAW_TRACEPOINT_PROBE` macro (if you did the exercises in Chapter 2, you’ll already have a suitable program you can use). You won’t need to explicitly attach the program in the Python code, as BCC will take care of it for you. Running this under strace, you should see a syscall similar to this: 

   ```shell
   bpf(BPF_RAW_TRACEPOINT_OPEN, {raw_tracepoint={name="sys_enter", prog_fd=6}}, 128) = 7 
   ```

   The tracepoint in the kernel has the name `sys_enter`, and the eBPF program with file descriptor 6 is being attached to it. From now on, whenever execution in the kernel reaches that tracepoint, it will trigger the eBPF program.