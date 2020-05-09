import random

def GenTrace3():
    # formula G(req => X(grant))
    trace_len = random.randint(150, 200)
    req = [0]*trace_len
    grant = [0]*trace_len

    for i in range(trace_len - 1):
        if random.randint(0, 10) < 1:
            req[i] = 1
            grant[i+1] = 1

    return (req, grant)

def GenTraces3():
    num_traces = random.randint(10, 20)
    f_req = open('req.facts', 'w')
    f_grant = open('grant.facts', 'w')
    for i in range(num_traces):
        req, grant = GenTrace3()
        trace_len = len(req)
        for j in range(trace_len):
            if req[j]: print('%d\t%d\t1' % (i, j), file=f_req)
            else: print('%d\t%d\t0' % (i, j), file=f_req)

            if grant[j]: print('%d\t%d\t1' % (i, j), file=f_grant)
            else: print('%d\t%d\t0' % (i, j), file=f_grant)

    f_req.close()
    f_grant.close()



def GenTrace_CS():
    num_proc = random.randint(2, 5)
    num_traces = random.randint(10, 20)
    trace_len = random.randint(30, 100)
    trace_files = [open("in_cs_"+str(i)+".facts", "w+") for i in range(num_proc)]
    for trace in range(num_traces):
        for timestamp in range(trace_len):
            in_cs = random.randint(0, num_proc-1)
            for proc in range(num_proc):
                if in_cs == proc:
                    trace_files[proc].write(str(trace)+"\t"+str(timestamp)+"\t"+str(1)+"\n")
                else:
                    trace_files[proc].write(str(trace)+"\t"+str(timestamp)+"\t"+str(0)+"\n")
    [i.close() for i in trace_files]



def GenTrace_G():
    num_traces = random.randint(500, 1000)
    trace_len = random.randint(1000, 2000)
    xfile = open("x.facts", "w+")
    for trace in range(num_traces):
        for timestamp in range(trace_len):
            xfile.write(str(trace)+"\t"+str(timestamp)+"\t"+str(1)+"\n")
    xfile.close()