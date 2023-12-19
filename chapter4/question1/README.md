使用strace和bpftool看到的insn_cnt并不相同？

首先使用`strace -e bpf ./hello-buffer-config.py`看到的指令条数为**44**条

![insn_cnt](strace.png)

之后使用`bpftool prog dump xlated name hello`得到的指令条数只有**42**条，dump出来的结果我放在了[xlated](xlated)