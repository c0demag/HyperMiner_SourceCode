# MTech-Thesis

The folder TempSpecsQuant contains the complete code required to synthesize a formula, and verifying it. 
The file Verifier.py in it is used to verify the formulas by invoking either SpecsGenerator_Generic or SpecsGenerator_Concrete for generation and BuildHorn to build horn clauses. 
The flags required for souffle can be changed in the file Test_Utilities.py in line 10.
The file SpecsGenerator_Generic generates random formulas by taking in as input the number of specifications required (by default it's 100 for generic and for concrete it's not required). While invoking Verifier.py, if Generic specifications are required, pass the number of specifications required as command line argument. (The default invocation of Verifier invokes SpecsGenerator_Concrete. To change this, change the header file imported in Verifier.py).

Folder Integration contains the code for benchmarking both the systems. The file LibConverter contains utilities used to convert the formulas of the souffle system type to libprop type. Benchmark.py can be invoked normally by following the given steps:
1. Change the Souffle flags from file TempSpecsQuant/Test_Utilities.py at line 10.
2. Clear the files in folders libprop/build and libprop/extras
3. Copy the trace to the folder TempSpecsQuant/ (Remove the dummy traces from this folder before copying new traces).
4. Change the number of epochs and number of specifications in each epoch required by modifying Integration/Benchmark.py's epoch list.
5. Run the following command: python3 Benchmark.py


The program will output the Formulas verified by souffle and will writeout the time taken by both systems in files named as Souffle_Time_$SomeDate$ and libprop_Time_$SomeDate$. 
The formulas verified and declared satisfied by libprop can be seen in the file libprop/build/bin/Satisfied_LibProp.

In libprop, the code to verify the formulas is in src folder named as TestLibProp.cpp. It reads the formulas, variables from files Specifications, Negated_Specifications, IntVars, BoolVars. And traces from .fact files and save them in internal data structures. 
Function parse all finally iterates on each formula, and in turn on every trace pair and verifies the formula for negative and positive examples.
