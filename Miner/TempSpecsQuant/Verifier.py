from Test_Utilities import *
from HyperLTLQuant import *
from BuildHorn import *
from SpecsGenerator_Concrete import *
import time, datetime



def Verify(specification):
    clear_files(False)
    spec = Formula(specification)
    negatedspec = spec.negate()
    CreateHornClauses(negatedspec, 0, True)
    Output = get_results(True)
    clear_files(False)
    if len(Output) == 0:
        CreateHornClauses(spec, 1, True)
        Output = get_results(True)
        if len(Output)>0:
            return True
    return False

num_specs = 100
if len(sys.argv)==2:
    num_specs = int(sys.argv[1])

Comp_Props = Generate(num_specs)
print("Synthesis Complete, Now Verifying")

all_file = open("All_Specifications"+str(datetime.datetime.now()), "w+")
sat_file = open("Satisfied_Specifications"+str(datetime.datetime.now()), "w+")

Comp_Props = list(Comp_Props)
for i in Comp_Props:
    st_time = time.time()
    if Verify(i):
        sat_file.write(str(i))
        sat_file.write("\n")
    all_file.write(str(i) + " : " + str(time.time()-st_time))
    all_file.write("\n")

all_file.close()
sat_file.close()
