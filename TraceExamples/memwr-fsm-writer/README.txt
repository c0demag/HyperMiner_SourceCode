two cores are executing in this setup (proc0, proc1)

proc0 has a FSM which randomly accesses data and proc1 has a user application running which 
aslo accesses some memory location.

there are two arbiters procarbiter and memarbiter which allow access for proc0 and proc1 to the memory location.
