from Test_Utilities import *
from HyperLTLQuant import *


def read_vars():
    os.system("ls *.facts > tmp")
    fi = open("tmp")
    lines = fi.readlines()
    lines = [line.strip()[:-6] for line in lines]
    varlst = []
    for i in lines:
        varlst.append(Variable(i, "1"))
        varlst.append(Variable(i, "2"))
    return varlst

def req_fill(tmp, Candidate):
    res = tmp.fill_hole(Candidate)
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
    tmp = Get_Random_Set(J)
    if tmp.holes()==1:
        if fill_func:
            req_fill(tmp, Get_Random(Functions))
        else:
            req_fill(tmp, Get_Random(Vars["int"]+Vars["bool"]))
    return

def Generate(num_specs):
    J.clear()
    Comp_Props.clear()
    NNFSet.clear()
    J.add(G(Hole()))
    Variables["int"] = read_vars()
    # if len(sys.argv)!=2:
    #     sys.exit("Usage: python3 SpecsGenerator.py [Num of Formulas Required]")
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

    # num_specs = int(sys.argv[1])
    print(Functions)
    while len(J) < (num_specs//5):
        fill(vars)          # Fill with variable
        fill(vars, True)      # Fill with function

    if len(Comp_Props)<num_specs:
        while len(Comp_Props) < num_specs:
            fill(vars)
    return Comp_Props


    
J, Comp_Props, NNFSet = set([G(Hole())]), set(), set()
Functions = [AND(Hole(), Hole()), OR(Hole(), Hole()), Implies(Hole(), Hole()), NOT(Hole()), X(Hole())]

Variables = {
    "int": [],
    "bool": []
    }
