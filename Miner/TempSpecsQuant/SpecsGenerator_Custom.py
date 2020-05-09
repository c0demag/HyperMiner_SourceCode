from TraceGenerator import *
from Test_Utilities import *
from HyperLTLQuant import *
import random, time, Globals, os, sys
from BuildHorn import *


def req_fill(tmp, Candidate, LoR):
    if LoR == 0:
        res = tmp.LHS.fill_hole(Candidate)
    else:
        res = tmp.RHS.fill_hole(Candidate)
    if res != -1:
        if tmp.holes() == 0:
            nnf_temp = ConvertToNNF(tmp)
            if nnf_temp not in NNFSet:
                Comp_Props.add(tmp)
                NNFSet.add(nnf_temp)
            
        elif tmp not in J:
            J.add(tmp)
        return tmp
    return -1

def fill(Vars, fill_func = False):
    while True:
        tmp = Get_Random_Set(J)
        LorR = random.randint(0, 9)%2
        if LorR == 0 and tmp.LHS.holes()==1:
            if fill_func:
                if req_fill(tmp, Get_Random(Functions), 0) != -1:
                    break
            else:
                if req_fill(tmp, Get_Random(Vars["int"]+Vars["bool"]), 0) != -1:
                    break
        elif LorR == 1 and tmp.RHS.holes()==1:
            if fill_func:
                if req_fill(tmp, Get_Random(Functions), 1) != -1:
                    break
            else:
                if req_fill(tmp, Get_Random(Vars["bool"]), 1) != -1:
                    break
    return

def Generate():
    if len(sys.argv)!=2:
        sys.exit("Usage: python3 SpecsGenerator.py [Num of Formulas Required]")
    vars = {"int": [], "bool": []}
    for i in range(len(Variables["int"])):
        for j in range(len(Variables["int"])):
            if i<j and Variables["int"][i].Name == Variables["int"][j].Name:
                vars["int"].append(Equality(Variables["int"][i], Variables["int"][j]))

    for i in Variables["bool"]:
        vars["bool"].append(Equality(i, True))
        vars["bool"].append(Equality(i, False))
    for i in range(len(Variables["bool"])):
        for j in range(len(Variables["bool"])):
            if i<j and Variables["bool"][i].Name == Variables["bool"][j].Name:
                vars["bool"].append(Equality(Variables["bool"][i], Variables["bool"][j]))

    num_specs = int(sys.argv[1])
    while len(J) < (num_specs//5):
        fill(vars)          # Fill with variable
        fill(vars, True)      # Fill with function

    if len(Comp_Props)<num_specs:
        while len(Comp_Props) <= num_specs:
            fill(vars)
    return Comp_Props



t1 = time.time()
J, Comp_Props, NNFSet = set([Implies(G(Hole()), G(Hole()))]), set(), set()
Functions = [AND(Hole(), Hole())]
Variables = {
    "int": [Variable("data1", "1"), Variable("data1", "2"), Variable("data2", "1"), Variable("data2", "2"), Variable("high_out", "1"), Variable("high_out", "2"), Variable("low_out", "1"), Variable("low_out", "2"), Variable("id1", "1"), Variable("id1", "2"), Variable("id2", "1"), Variable("id2", "2")],
    "bool": [Variable("sel", "1"), Variable("sel", "2")]
    }
Num_Funcs, Num_Vars = len(Functions), len(Variables)
Output = Generate()
print("Time to generate ", len(Comp_Props), " specifications : ", time.time()-t1)


all_file = open("All_Specifications", "w+")
sat_file = open("Satisfied_Specifications", "w+")

Comp_Props = list(Comp_Props)
for i in range(len(Comp_Props)):
    if i%10 == 0:
        print("Processed " + str(i) + " specifications")
    st_time = time.time()
    clear_files(False)
    spec = Formula(Comp_Props[i])
    negatedspec = spec.negate()
    CreateHornClauses(negatedspec, 0, True)
    Output = get_results(True)
    clear_files(False)
    if len(Output) == 0:
        CreateHornClauses(spec, 1, True)
        Output = get_results(True)
        if len(Output)>0:
            print(spec)
            sat_file.write(str(spec))
            sat_file.write("\n")
    clear_files(False)
    all_file.write(str(spec) + " : " + str(time.time()-st_time))
    all_file.write("\n")

all_file.close()
sat_file.close()