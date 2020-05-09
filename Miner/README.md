Miner

This directory contains the Miner module from the HyperMiner framework.

Directory Description:
  1. TempSpecsQuant: Contains the code for mining the HyperLTL properties and also converting them to Horn Clause for verification using Souffle. 
  2. libprop: Contains our C++ based verifier for the HyperLTL properties
  3. Integration: Contains the code to run all the experiments. 

To run the experiments, navigate to the integration folder using the following command:
```bash
cd HyperMiner_SourceCode/Integration
```
The files Benchmark_Concrete.py and Benchmark_Random are used to run the experiments for the template version of the miner and the random version respecitively.

To run the experiment for the template version, following is the command:
```bash
python3 -u Benchmark_Concrete.py [Experiment_Name] [Experiment_Version]
```
The Experiment_Name must be the name of the experiment. Make sure that the name typed in here must match a folder in HyperMiner_SourceCode/TraceExamples/.

The Experiment_Version will be:

  0 for Listing out only the formulas generated, this option doesn't perform any verification but is used to check the miner only.
  1 for running only the Souffle experiments
  2 for running only the libprop experiments
  3 for running both Souffle and libprop experiments

Note: The program will print the logs and build outputs on the terminal. To redirect them to a logfile: 
```bash
 python3 -u Benchmark_Concrete.py [Experiment_Name] [Experiment_Version] > logfile 2>&1
 ```
If you don't want the logs, you can replace logfile by /dev/null.

To run the experiments for the random version, just replace the file name from Benchmark_Concrete.py to Benchmark_Random.py, all other instructions are same as template version.

A sample command to list out the properties generated from template for experiment aes_test will be:
```bash
python3 -u Benchmark_Concrete.py aes_test 0 > logfile 2>&1
```

As result of running versions 1-3 of the experiment, the program will generate some files in the folder Integration itself, which will be:
  1. Satisfied_ToolName_ExpName - The file will contain the properties given out as satisfied by ToolName (either Souffle or libprop) for experiment ExpName
  2. ToolName_Time_ExpName - The file will contain the time taken to verify the properties by tool ToolName and for experiment ExpName.
  
Note: Performing souffle experiments may take hours, hence it'll be suggested to run the program in background.
