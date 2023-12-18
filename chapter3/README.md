# Exercises for Chapter3

Here are a few things to try if you want to explore BPF programs further:

1. Try using `ip link` commands like the following to attach and detach the XDP program:

    ```shell
    $ ip link set dev eth0 xdp obj hello.bpf.o sec xdp
    $ ip link set dev eth0 xdp off
    ```

2. Run any of the BCC examples from Chapter 2. While the program is running, use a second terminal window to inspect the loaded program using bpftool. Here's an example of what I saw by running the **hello-map.py** example:

    ```shell
    $ bpftool prog show name hello
    197: kprobe name hello tag ba73a317e9480a37 gpl
    		loaded_at 2022-08-22T08:46:22+0000 uid 0 
    		xlated 296B jited 328B memlock 4096B map_ids 65 
    		btf_id 179 
    		pids hello-map.py(2785)
    ```

    You can also use `bpftool prog dump` commands to see the bytecode and machine code versions of those programs.

3. Run **hello-tail.py** from the chapter2 directory, and while it's running, take a look at the programs it loaded. You'll see that each tail call program is listed individually, like this:

   ```shell
   $ bpftool prog list 
   ... 
   120: raw_tracepoint name hello tag b6bfd0e76e7f9aac gpl 
   		loaded_at 2023-01-05T14:35:32+0000 uid 0 
   		xlated 160B jited 272B memlock 4096B map_ids 29 
   		btf_id 124 
   		pids hello-tail.py(3590) 
   121: raw_tracepoint name ignore_opcode tag a04f5eef06a7f555 gpl 
   		loaded_at 2023-01-05T14:35:32+0000 uid 0 
   		xlated 16B jited 72B memlock 4096B 
   		btf_id 124 
   		pids hello-tail.py(3590) 
   122: raw_tracepoint name hello_exec tag 931f578bd09da154 gpl 
   		loaded_at 2023-01-05T14:35:32+0000 uid 0 
   		xlated 112B jited 168B memlock 4096B 
   		btf_id 124 
   		pids hello-tail.py(3590) 
   123: raw_tracepoint name hello_timer tag 6c3378ebb7d3a617 gpl 
   		loaded_at 2023-01-05T14:35:32+0000 uid 0 
   		xlated 336B jited 356B memlock 4096B 
   		btf_id 124 
   		pids hello-tail.py(3590)
   ```

   You could also use `bpftool prog dump xlated` to look at the bytecode instructions and compare them to what you saw in "BPF to BPF Calls" on page 54.

4. **Be careful with this one, as it may be best to simply think about why this happens rather than trying it!** If you return a 0 value from an XDP program, this corresponds to `XDP_ABORTED`, which tells the kernel to abort any further processing of this packet. This might seem a bit counterintuitive given that the 0 value usually indicates success in C, but that’s how it is. So, if you try modifying the program to return 0 and attach it to a virtual machine’s eth0 interface, all network packets will get dropped. This will be somewhat unfortunate if you’re using SSH to attach to that machine, and you’ll likely have to reboot the machine to regain access! 

   You could run the program within a container so that the XDP program is attached to a virtual Ethernet interface that only affects that container and not the whole virtual machine. There’s an example of doing this at https://github.com/lizrice/lb-from-scratch.