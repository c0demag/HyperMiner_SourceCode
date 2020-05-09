from HyperLTLQuant import *
import re
import pickle
import Globals
import os
import time
import subprocess
from Test_Utilities import *
from TraceGenerator import *
from BuildHorn import *


def check_satisfiability(spec):
  negatedspec = spec.negate()
  CreateHornClauses(negatedspec, 0, True)
  Output = get_results(True)
  if len(Output) == 0:
    CreateHornClauses(spec, 1, True)
    Output = get_results(True)
    if len(Output)>0:
      print(spec)


clear_files()

os.chdir("../../TraceExamples/peterson")
os.system("make clean >> /dev/null")
os.system("make >> /dev/null")
os.system("./run >> /dev/null")
os.system("cp *.facts ../../MTech-Thesis/TempSpecsQuant/")
os.chdir("../../MTech-Thesis/TempSpecsQuant/")


convert_trace_to_current(["ap_crit0", "ap_crit1"])
ap_crit0 = Equality(Variable("ap_crit0","1"), True)
ap_crit1 = Equality(Variable("ap_crit1","1"), True)
spec = Formula(G(NOT(AND(ap_crit0, ap_crit1))))

check_satisfiability(spec)
clear_files()


############################## TEST CASES FOR TEST-FAIL ####################################################
'''
  PROPERTIES:
    1. G(init ⟶ X(serve))
    2. G(fail ⟶ X(init))
'''

os.chdir("../../TraceExamples/try-fail")
os.system("make clean >> /dev/null")
os.system("make >> /dev/null")
os.system("./run >> /dev/null")
os.system("cp *.facts ../../MTech-Thesis/TempSpecsQuant/")
os.chdir("../../MTech-Thesis/TempSpecsQuant/")


init = Equality(Variable("ap_init","1"), True)
serve =Equality( Variable("ap_serve","1"), True)
fail = Equality(Variable("ap_fail","1"), True)
convert_trace_to_current(["ap_init", "ap_serve", "ap_fail"])
spec = Formula(G(Implies(init, X(serve))))
check_satisfiability(spec)

#


spec = Formula(G(Implies(fail, X(init))))
check_satisfiability(spec)
clear_files()


################
GenTraces3()
req = Equality(Variable("req", "1"), True)
grant = Equality(Variable("grant", "1"), True)
spec = Formula(G(Implies(req, X(grant))))
check_satisfiability(spec)
clear_files()


##########################
GenTrace_CS()
os.system("ls *.facts > tmp")
fi = open("tmp")
lines = fi.readlines()
lines = [line.strip() for line in lines]
num_processes = len(lines)
form_list = []
for i in range(num_processes):
  for j in range(i+1, num_processes):
    if i!=j:
      var1 = Equality(Variable("in_cs_" + str(i), "1"), True)
      var2 = Equality(Variable("in_cs_" + str(j), "1"), True)
      form_list.append(AND(var1, var2))
final_form = form_list[0]
for i in range(1, len(form_list)):
  final_form = AND(form_list[i], final_form)
spec = Formula(NOT(final_form))
check_satisfiability(spec)
clear_files()


init_time = time.time()
GenTrace_G()
x = Equality(Variable("x", "1"), True)
spec = Formula(G(x))
check_satisfiability(spec)

clear_files()
print(time.time()-init_time)

print("Tests Passed")