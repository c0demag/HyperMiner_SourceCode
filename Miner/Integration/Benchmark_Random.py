import os, time, datetime, sys

if len(sys.argv) != 3:
    print("\nUsage: python3 Benchmark_Random.py Experiment_Name Experiment_Requirement \nWhere requirement is 3 for souffle and libprop experiment both, 1 for souffle only, 2 for libprop only and 0 to show only the generated specifications\n")
    sys.exit(0)

def Verify(specification):
    clear_files(False)
    start_time = time.time()
    spec = Formula(specification)
    negatedspec = spec.negate()
    CreateHornClauses(negatedspec, 0, True)
    Output = get_results(True)
    clear_files(False)
    if len(Output) == 0 or Output == []:
        CreateHornClauses(spec, 1, True)
        Neg_Output = get_results(True)
        if len(Neg_Output)>0 and Neg_Output != ['']:
            return (True, time.time()-start_time)
    return (False, time.time()-start_time)

def removeUnderScores(st):
    return ''.join(st.split('_'))


os.system("cp -f ../TempSpecsQuant/* .")


TSQ_List = ["Arith.py", "ClauseAST.py", "HyperLTLQuant.py", "SpecsGenerator_Concrete.py", "SpecsGenerator_Generic.py", "Tester.py", "Verifier.py", "BuildHorn.py", "Globals.py", "SingleTests.py", "SpecsGenerator_Custom.py", "Test_Utilities.py", "TraceGenerator.py", "__init__.py"]

from HyperLTLQuant import *
from SpecsGenerator_Generic import *
from LibConverter_Generic import *
from BuildHorn import *


experiments = sys.argv[1:-1]
for ename in experiments:
    if not os.path.isdir("../../TraceExamples/" + ename):
        print(ename + " not a valid experiment name\n")
        sys.exit(0)
libprop_file_list = ["Specifications", "Negated_Specifications", "IntVars", "BoolVars", "*.facts"]

for exp_name in experiments:

    for rem_file in libprop_file_list:
        os.system("rm -rf "+rem_file)
    os.system("rm -rf *.csv")
    os.system("rm -rf TraceEnd.facts")
    
    os.system("cp ../../TraceExamples/" + exp_name + "/*.facts .")
    

    curr_dir_files = os.listdir(".") 
    for filename in curr_dir_files:
        if filename.endswith(".facts"): 
            if filename == removeUnderScores(filename):
                continue
            os.system("mv " + filename + " " + removeUnderScores(filename))


    Specifications = list(Generate(100))
    print("Generated ", len(Specifications), " specifications")

    if sys.argv[-1] == "0" or sys.argv[-1] == 0:
        for i in Specifications:
            print(i)

    ############################################################################
    ########################### Souffle Verification ###########################
    ############################################################################
    if sys.argv[-1] in ["1", "3"] or sys.argv[-1] == 1 or sys.argv[-1] == 3:
        print("Working on Souffle Experiment: ", exp_name)
        Souffle_Start_Time = time.time()
        sat_string = ""
        count = 0
        Clear_Globals()
        for spec in Specifications:
            print(spec, datetime.datetime.now())
            (IsVerified, VerificationTime) = Verify(spec)
            if IsVerified:
                print(spec)
                sat_string += str(spec)+"\n"
                count += 1
    
        Souffle_Time_File = open("Souffle_Time_" + exp_name, "w+")
        Souffle_Verified_File = open("Satisfied_Souffle_" + exp_name, "w+")
    
        Souffle_Time_File.write("Total time to verify " + str(len(Specifications)) + " specifications : " + str(time.time() - Souffle_Start_Time) + " for experiment : " + exp_name + " with " + str(count)+ " satisfied\n")
        Souffle_Verified_File.write(sat_string)
    
        Souffle_Verified_File.close()
        Souffle_Time_File.close()
        os.system("rm -rf TraceEnd.facts")
        os.system("rm -rf *.csv")
        os.system("rm -rf *.dl")


    ############################################################################
    ########################### libprop Verification ###########################
    ############################################################################
    if sys.argv[-1] in ["2", "3"] or sys.argv[-1] == 2 or sys.argv[-1] == 3:
        print("Working on libprop experiment : ", exp_name)
        Converter(Specifications)

        if not os.path.isdir("../libprop/extras"):
            os.system("mkdir ../libprop/extras/")
        
        for i in libprop_file_list:
            os.system("cp -f " + i + " ../libprop/extras/")
    
        os.chdir("../libprop/")
    
        if not os.path.isdir("./build"):
            os.system("mkdir build")
        os.chdir("./build")
        os.system("rm -rf *")
        os.system("cmake .. -DCMAKE_BUILD_TYPE=Release")
        os.system("make")
    
        if not os.path.isdir("./bin"):
            print("Error in libprop build, try again")
            sys.exit(0)
        os.chdir("./bin")
    
        libprop_Start_Time = time.time()
        os.system("./runlibprop")
        libprop_End_Time = time.time()
    
        os.system("cp Satisfied_LibProp ../../../Integration/")

        os.chdir("../../../Integration")

        os.system("mv Satisfied_LibProp Satisfied_libProp_" + exp_name)

        libprop_Time_File = open("libprop_Time_" + exp_name, "w+")
        libprop_Time_File.write("Total time to verify " + str(len(Specifications)) + " specifications : " + str(libprop_End_Time - libprop_Start_Time) + " for experiment : " + exp_name +  "\n")
        libprop_Time_File.close()


for to_del in TSQ_List+libprop_file_list:
    os.system("rm -f " + to_del)
os.system("rm -rf tmp")
os.system("rm -rf __pycache__")
os.system("rm -rf LTL.dl")
os.system("rm -rf souffle*")
