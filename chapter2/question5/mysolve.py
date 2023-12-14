#!/usr/bin/python3  
from bcc import BPF
from time import sleep

program = r"""
BPF_HASH(counter_table);

RAW_TRACEPOINT_PROBE(sys_enter) {
    u64 counter = 0;
    u64 opcode = ctx->args[1];
    u64 *p;
    
    p = counter_table.lookup(&opcode);
    
    if(p != 0) {
        counter = *p;
    }
    counter++;
    counter_table.update(&opcode, &counter);
}
"""

b = BPF(text=program)

# Attach to a tracepoint that gets hit for all syscalls 
# b.attach_raw_tracepoint(tp="sys_enter", fn_name="hello")

while True:
    sleep(2)
    s = ""
    for k,v in b["counter_table"].items():
        s += f"syscall {k.value}: {v.value}\t"
    print(s)
