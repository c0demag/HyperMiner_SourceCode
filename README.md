HyperMiner

The repository contains the framework - HyperMiner for mining HyperLTL properties using execution traces. 

The directory description is as follows: 
  1. Miner - Contains the code for mining HyperLTL formulas and Verification.
  2. TraceExamples - Contains the traces extracted.
  3. Results - Contains the results of the various experiments conducted.
  
Change directory to `HyperMiner_SourceCode` project folder and run `git submodule update --init --recursive` to update the sub-modules.

As some initial steps, run the script setup.sh as follows: 
  ```bash
  sudo ./setup.sh
  ```
If the command gives error, run the following, and then the above command:
```bash
chmod +x setup.sh
  ```

Example traces have been provided in TraceExamples and TraceExamplesCustomCov directories already. If you wish to regenerate the traces please refer to the README.md file at [fuzztest-tracegen/fuzztest/README.md](https://github.com/skmuduli92/fuzztest-tracegen/blob/4a40435cd49e7e5820bd29ccf102c37fc63f4520/fuzztest/README.md)
