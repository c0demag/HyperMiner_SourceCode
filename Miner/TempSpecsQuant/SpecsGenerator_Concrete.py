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

def Generate(dummy = 100):
    Comp_Props=set()
    Variables["int"] = read_vars()
    vars = {"int": [], "bool": []}
    for i in range(len(Variables["int"])):
        for j in range(len(Variables["int"])):
            if i<j and Variables["int"][i].Name == Variables["int"][j].Name:
                vars["int"].append(Equality(Variables["int"][i], Variables["int"][j]))

    # for i in Variables["bool"]:
    #     vars["bool"].append(Equality(i, True))
    #     vars["bool"].append(Equality(i, False))
    for i in range(len(Variables["bool"])):
        for j in range(len(Variables["bool"])):
            if i<j and Variables["bool"][i].Name == Variables["bool"][j].Name:
                vars["bool"].append(Equality(Variables["bool"][i], Variables["bool"][j]))

    Combined_Vars = vars["int"] + vars["bool"]

    for i in Combined_Vars:
        for j in Combined_Vars:
            if i!=j:
                Comp_Props.add(G(Implies(i, j)))
                Comp_Props.add(Implies(G(i), G(j)))

    return Comp_Props


Comp_Props = set()

Variables = {
    "int": [],
    "bool": []
    }

