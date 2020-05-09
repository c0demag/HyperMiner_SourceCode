
#include<bits/stdc++.h>
#include<pthread.h>

#include "formula.h"
#include "parse_util.h"
#include "formula_util.h"
#include "trace.h"

using namespace HyperPLTL;
using namespace std;


unsigned max(unsigned a, unsigned b){
    return a>b ? a : b;
}

//Function to read files and get the variables name by type = int or bool. 
vector<string> getVarsByType(string type){
    vector<string>varints;
    ifstream varfile;
    string x;
    varfile.open(type);
    while (varfile >> x) {
        if(x!="" && x!="\n")
            varints.push_back(x);
    }
    varfile.close();
    return varints;
}

// Function to read the traces from trace files. Map is of format Traces[TraceNumber][Variable_Name]<Vector of <time, value> pairs>
map<unsigned, map<string, vector<pair<unsigned, unsigned>>>> readFileTraces(){
  vector<string>varints = getVarsByType("IntVars");
  vector<string>varprops = getVarsByType("BoolVars");
  map<unsigned, map<string, vector<pair<unsigned, unsigned>>>>read_traces;

  ifstream varfile;
  for(unsigned i=0;i<varints.size();i++){
    unsigned tr, ti, val;
    string var = varints[i];
    varfile.open(varints[i]+".facts");
    string x;
    while (varfile >> x) {
        assert(x!="\n" && x!="" && x!="\0");
        tr = stoi(x);
        varfile >> x;
        ti = stoi(x);
        varfile >> x;
        val = stoi(x);
        if ( read_traces.find(tr) == read_traces.end() || read_traces[tr].find(var) == read_traces[tr].end())
            read_traces[tr][var] = vector<pair<unsigned, unsigned>>();
        read_traces[tr][var].push_back(make_pair(ti, val));
    }
    varfile.close();
  }
  for(unsigned i=0;i<varprops.size();i++){
    unsigned tr, ti, val;
    string var = varprops[i];
    varfile.open(varprops[i]+".facts");
    string x;
    while (varfile >> x) {
        assert(x!="\n" && x!="" && x!="\0");
        tr = stoi(x);
        varfile >> x;
        ti = stoi(x);
        varfile >> x;
        val = stoi(x);
        if ( read_traces.find(tr) == read_traces.end() || read_traces[tr].find(var) == read_traces[tr].end())
            read_traces[tr][var] = vector<pair<unsigned, unsigned>>();
        read_traces[tr][var].push_back(make_pair(ti, val));
    }
    varfile.close();
  }
  return read_traces;
}


// Function to read properties from file to verify
vector<string> read_formulas(string filename){
    string x;
    vector<string>result;
    ifstream varfile;
    varfile.open(filename);
    while (std::getline(varfile, x)) {
        if(x!=" " && x!="\n")
            result.push_back(x);
    }
    varfile.close();
    return result;
}


vector<string> Verify_In_Range(unsigned start_index, unsigned end_index, vector<PTrace> trace_vec, vector<string> formulas, vector<string> negated_formulas, PVarMap varmap){
    vector<string> satisfied_Formulas;

    // Loop over each property in the formulas list
    //cout<<start_index<<" "<<end_index<<endl;
    for(unsigned it = start_index; it <= end_index && it < formulas.size() && it >= 0; it++){

        // Parsing the property
        PHyperProp property =  parse_formula(formulas[it], varmap);
        PHyperProp negated_property =  parse_formula(negated_formulas[it], varmap);

        bool has_negatives = false;
        bool satisfied = false;

        // Iterating over trace pairs.
        for(unsigned tr1=0;tr1<trace_vec.size() && !has_negatives;tr1++){
            // Iterating for second trace
            for(unsigned tr2 = tr1+1; tr2<trace_vec.size() && !has_negatives; tr2++){
                if(tr1 == tr2)  continue;
                
                // Handling unequal traces so that utility function runs till lower tracelength only.
                TraceList tracelist;
                if(trace_vec[tr1]->length() < trace_vec[tr2]->length())
                    tracelist = TraceList({trace_vec[tr1], trace_vec[tr2]});
                else
                    tracelist = TraceList({trace_vec[tr2], trace_vec[tr1]});

                // Evaluate the property over tracelist
                bool negs = evaluateTraces(negated_property, tracelist);
                if(negs)
                    has_negatives = true;
                else if(!satisfied){
                    bool poss = evaluateTraces(property, tracelist);
                    satisfied = satisfied || poss;
                }
            } // End of loop for Tr2
        }   // End of loop for Tr1
        if(satisfied && !has_negatives){
           satisfied_Formulas.push_back(formulas[it]);
        }
    } // End of loop for formulas
    return satisfied_Formulas;
}


// Function to verify the formulas one by one picking pair of trace at a time
void ParseAll() {
    //Populate the variable names, and trace structures
    map<unsigned, map<string, vector<pair<unsigned, unsigned>>>> traces = readFileTraces();
    unsigned commontraceend = INT_MAX;
    for(auto i: traces)
        for(auto j: i.second){
            sort(j.second.begin(), j.second.end());
	    commontraceend = min(unsigned(j.second.size()), commontraceend);
	}
    //cout<<commontraceend<<endl;
    vector<string> formulas = read_formulas("Specifications");
    vector<string> negated_formulas = read_formulas("Negated_Specifications");
    vector<string> int_vars = getVarsByType("IntVars");
    vector<string> bool_vars = getVarsByType("BoolVars");

    
    assert(formulas.size() == negated_formulas.size() && formulas.size() > 0);
    assert(int_vars.size() > 0 || bool_vars.size() > 0);

    // Populate the var map
    PVarMap varmap = std::make_shared<VarMap>();
    for (auto var: int_vars)
        varmap->addIntVar(var);
    for (auto var: bool_vars)
        varmap->addPropVar(var);

    // Populating traces
    PHyperProp tmpprop =  parse_formula(formulas[0], varmap);
    vector<PTrace> trace_vec;
    for(unsigned trnum = 0; trnum<traces.size(); trnum++){
        PTrace trace1(new Trace(bool_vars.size(), int_vars.size()));
        for(auto vars: int_vars){
            unsigned xid = tmpprop->getVarId(vars);
	    for(unsigned tmpite = 0; tmpite<traces[trnum][vars].size() && tmpite<commontraceend; tmpite++){
            	auto pr = traces[trnum][vars][tmpite];
                trace1->updateTermValue(xid, pr.first, pr.second);
            }
        }
        for(auto vars: bool_vars){
            unsigned xid = tmpprop->getPropId(vars);
            for(unsigned tmpite = 0; tmpite<traces[trnum][vars].size() && tmpite<commontraceend; tmpite++){
		auto pr = traces[trnum][vars][tmpite];
                assert(pr.second%2==pr.second);
                trace1->updatePropValue(xid, pr.first, pr.second);
            }
        }
        trace_vec.push_back(trace1);
    }

    // Do Verification
    vector<vector<string>> res;
    unsigned cproc = std::thread::hardware_concurrency() - 2;
    if(cproc<=1){
        unsigned st_ind = 0;
        unsigned end_ind = formulas.size()-1;
        res.push_back(Verify_In_Range(st_ind, end_ind, trace_vec, formulas, negated_formulas, varmap));
    }
    else{       // Concurrency here
        cout<<"Running on "<<cproc<<" cores \n";
        vector<std::future< vector <string> > >promises;
        unsigned block_size = 1 + (formulas.size()/cproc);
        future<vector<string>> future1;
        vector<unsigned>start_indexes, end_indexes;
        for(unsigned i=1; i<=cproc;i++){
            start_indexes.push_back((i-1)*block_size);
            end_indexes.push_back((i)*block_size -1);
        }

        for(unsigned i=0; i<cproc;i++){
            future1 = std::async(std::launch::async, Verify_In_Range, std::ref(start_indexes[i]), std::ref(end_indexes[i]), std::ref(trace_vec), std::ref(formulas), std::ref(negated_formulas), std::ref(varmap));
            promises.emplace_back(std::move(future1));
        }
        for(unsigned i=0;i<cproc;i++){
            res.push_back(promises[i].get());
        }
    }

    // File for writing satisfied formulas
    ofstream file_sat;
    file_sat.open("Satisfied_LibProp", ios::out | ios::trunc);
    for(auto item: res){
        if(item.size() > 0){
            for(auto satprop: item){
                file_sat<<satprop<<endl;
            }
        }
    }
    file_sat.close();

}

int main(){
    ParseAll();
    return 0;
}
