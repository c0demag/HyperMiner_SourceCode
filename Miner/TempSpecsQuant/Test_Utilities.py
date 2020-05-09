import re
import Globals
import os
import subprocess
import copy
import random


def get_results(IsFormula = False):
    os.system("souffle -c -j auto  LTL.dl")
    filename = "TempSpec.csv"
    if IsFormula:
        filename = "Formula1.csv"
    cs = open(filename)
    lines = cs.readlines()
    results = [line.rstrip('\n') for line in lines]
    cs.close()
    return results

def clear_files(removeFactsDl = True):
    if removeFactsDl:
        os.system("rm -f *.facts")
    os.system("rm -f *.dl")
    os.system("rm -f *.csv")
    os.system("rm -f tmp")

def Get_TraceData():
    os.system("ls *.facts > tmp")
    fi = open("tmp")
    lines = fi.readlines()
    lines = [line.strip() for line in lines]
    traceend = 99999999
    num_traces = 0
    for filename in lines:
        filehand = open(filename)
        facts = filehand.readlines()

        dict = {}
        for i in facts:
            i = re.split(r'\t+', i)
            i = [int(j) for j in i]
            tNum, timestamp = i[0], i[1]
            if tNum not in dict:
                dict[tNum] = timestamp
            else:
                dict[tNum] = max(timestamp, dict[tNum])

        if num_traces != 0:
            assert len(dict) == num_traces
        else:
            num_traces = len(dict)

        traces = []
        for key in dict:
            traceend = min(traceend, dict[key])
            traces.append(key)
            assert key < num_traces
        
        traces.sort()
        assert traces == [i for i in range(num_traces)]

        filehand.close()
    fi.close()
    
    return [traceend for i in range(num_traces)]
    

def convert_trace_to_current(lst):
    for i in lst:
        ftrue = open(i+"_true.facts", "r")
        ffalse = open(i+"_false.facts", "r")
        t = ftrue.readlines()
        f = ffalse.readlines()
        tfacts = [re.split(r'\t+', li) for li in t]
        tfacts = [ [int(j) for j in i] for i in tfacts ]
        for j in tfacts:
            j.append(1)
        ffacts = [re.split(r'\t+', li) for li in f]
        ffacts = [ [int(j) for j in i] for i in ffacts ]
        for j in ffacts:
            j.append(0)
        facts = tfacts + ffacts
        facts.sort()
        fact_file = open(i+".facts", "w+")
        for j in facts:
            st=""
            for k in range(len(j)-1):
                st+=str(j[k])+"\t"
            st+=str(j[-1])
            fact_file.write(st)
            fact_file.write("\n")
        fact_file.close()
        ftrue.close()
        ffalse.close()
    os.system("rm -rf *_true.facts")
    os.system("rm -rf *_false.facts")
    return


def Get_Random(lst):
    return copy.deepcopy(lst[random.randint(0, len(lst)-1)])

def Get_Random_Set(s):
    return copy.deepcopy(random.choice(tuple(s)))

def Alter(ob):
    if (not hasattr(ob, 'cl')) or (ob.cl != "Equality" and ob.cl != "InEquality"):
        return ob
    if isinstance(ob.RHS, int) and ob.RHS not in [True, False]:
        ob.RHS = random.randint(0, 10)
    if isinstance(ob.RHS, bool):
        ob.RHS = Get_Random([True, False])
    return ob
        
