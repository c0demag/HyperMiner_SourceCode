from HyperLTLQuant import *
from SpecsGenerator_Concrete import *



def ConvertToLibprop(spec, approach):
    st = ""
    if spec.cl == "Formula":
        st = ConvertToLibprop(spec.Spec, approach)
    elif spec.cl == "Equality":
        if spec.RHS == True:
            st = spec.LHS.Name + "." + str(spec.LHS.Trace - 1)
        elif spec.RHS == False:
            st = "( NOT " + spec.LHS.Name + "." + str(spec.LHS.Trace - 1) + " )"
        else:
            st = "( EQ " + spec.LHS.Name + " )"
    elif spec.cl == "InEquality":
        if spec.RHS == False:
            st = spec.LHS.Name + "." + str(spec.LHS.Trace - 1)
        elif spec.RHS == True:
            st = "( NOT " + spec.LHS.Name + "." + str(spec.LHS.Trace - 1) + " )"
        else:
            st = "( NOT ( EQ " + spec.LHS.Name + " ) )"
    elif spec.cl == "Implies":
        st = "( IMPLIES " + ConvertToLibprop(spec.LHS, (approach+1)%2) + ConvertToLibprop(spec.RHS, approach) + " )"
    elif spec.cl in ["AND", "OR"]:
        if spec.cl == "AND" and spec.WasImplication:
            st = "( AND " + ConvertToLibprop(spec.LHS, (approach+1)%2) + ConvertToLibprop(spec.RHS, approach) + " )"
        else:
            st = "( " + spec.cl + " " + ConvertToLibprop(spec.LHS, approach) + ConvertToLibprop(spec.RHS, approach) + " )"
    elif spec.cl in ["G", "F", "X"]:
        if approach == 0:
            st = "( " + spec.cl + "- " + ConvertToLibprop(spec.RHS, approach) + " )"
        else:
            st = "( " + spec.cl + "+ " + ConvertToLibprop(spec.RHS, approach) + " )"
    elif spec.cl == "NOT":
        st = "( NOT " + ConvertToLibprop(spec.RHS, approach) + " )"
    return st


def Converter(Output_List):
    Output_List = list(Output_List)

    # Exporting formulas to files
    form_file = open("Specifications", "w+")
    neg_file = open("Negated_Specifications", "w+")

    for formula in Output_List:
        form_file.write(ConvertToLibprop(formula, 1) + "\n")
        neg_file.write(ConvertToLibprop(formula.negate(), 0) + "\n")
    
    form_file.close()
    neg_file.close()
    
    Variables = {
            "int": read_vars(),
            "bool": []
            }

    # Exporting Integral Variables to file
    IVar_File = open("IntVars", "w+")
    IVar_Set = set([i.Name for i in Variables["int"]])
    for var in IVar_Set:
        IVar_File.write(var + "\n")
    IVar_File.close()

    # Exporting Boolean Variables to file
    BVar_File = open("BoolVars", "w+")
    BVar_Set = set([i.Name for i in Variables["bool"]])
    for var in BVar_Set:
        BVar_File.write(var + "\n")
    BVar_File.close()
