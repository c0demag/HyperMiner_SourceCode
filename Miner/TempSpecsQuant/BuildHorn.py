from HyperLTLQuant import *
from Test_Utilities import *
import Globals
import random
import os


def Clear_Globals():
    Globals.init([])

def CreateHornClauses(Specification, approach, IsFormula = False):
    Globals.init(Globals.TraceEnds)
    if Globals.TraceEnds == []:
        Globals.TraceEnds = Get_TraceData()
    
    LTLfile = open("LTL.dl", "w")
    TraceEndFile = open("TraceEnd.facts", "w")


    NN = ConvertToNNF(Specification)    
    NN.build_horn(approach, IsFormula)
    
    declarer("TraceEnd", 2, True)
    for i in range(len(Globals.TraceEnds)):
        TraceEndFile.write(str(i) + "\t" + str(min(Globals.TraceEnds)) + "\n")                 # Change TraceEnd here

    declarer("CommonEnd", 1)

    for i in Globals.declarations:
        LTLfile.write(str(i))
        LTLfile.write("\n")
    
    LTLfile.write("CommonEnd(" + str(min(Globals.TraceEnds))+").\n")

    LTLfile.write("\n")
    LTLfile.write("\n")

    magic_string = ".pragma \"magic-transform\" \""
    for i in Globals.magic_transform:
        magic_string += str(i) + ", "
    magic_string = magic_string[:-2] + "\"" 
    LTLfile.write(magic_string)


    LTLfile.write("\n")
    LTLfile.write("\n")

    Globals.rules.reverse()
    for i in Globals.rules:
        if i != "\n":
            LTLfile.write(str(i)+".")
        LTLfile.write("\n")

    LTLfile.close()
    TraceEndFile.close()    
    return
