import Globals

class HornClause():
    pass

class Clause(HornClause):
    def __init__(self, head, body):
        self.cl="Clause"
        self.Head=head
        self.Body=body
    def __repr__(self):
        return str(self.Head)+":-"+str(self.Body)

class Body():
    def __init__(self, lst):
        self.cl="Body"
        self.Relations=lst
    def __repr__(self):
        st=""
        for i in self.Relations:
            st+=str(i)+","
        return st[:-1]

class Relation(HornClause):
    def __init__(self, name, var):
        self.cl="Relation"
        self.Name=name
        self.Vars=var
    def __repr__(self):
        st= self.Name+"("
        for i in self.Vars:
            st+=str(i)+","
        return st[:-1]+")"
            

class Relate(Relation):     #Defines equalities and inequalities in Horn Clauses
    def __init__(self, lhs, etype, rhs=None):
        self.lhs=lhs
        self.rhs=rhs
        self.type=etype             # 0 for Inequality and 1 for equality
        self.cl="Relate"
    def __repr__(self):
        if self.type=="equal":
            return str(self.lhs)+"!="+str(self.rhs)
        elif self.type=="not equal":
            return str(self.lhs)+"="+str(self.rhs)
        elif self.type=="or":
            return "("+ str(self.lhs) + ", " + str(self.rhs) +")"
        elif self.type=="not":
            return "!"+str(self.rhs)

def fresh_variable():
    Globals.counter=Globals.counter+1
    if Globals.counter == 26:
        Globals.length = Globals.length + 1
        Globals.counter = 0
    if chr(65+Globals.counter)*Globals.length=='T' or chr(65+Globals.counter)*Globals.length=='T1':
        Globals.counter=Globals.counter+1
        if Globals.counter == 26:
            Globals.length = Globals.length + 1
            Globals.counter = 0
    return chr(65+Globals.counter)*Globals.length

def ClauseOR(x, y):
    return "("+str(x)+";"+str(y)+")"
def ClauseAND(x, y):
    return str(x)+", "+str(y)
def ClauseNOT(x):
    return "!"+str(x)

def declarer(name, num_args, is_input=False):
    dec_st = ".decl "+name+"("
    start_var = "a"
    for _ in range(num_args):
        dec_st+=start_var+": number, "
        start_var = chr(ord(start_var)+1)
    dec_st = dec_st[:-2]+")"
    if not is_input and name!="CommonEnd":
        dec_st+=" brie"
        Globals.declarations.append(dec_st)
    elif is_input:
        Globals.declarations.append(dec_st)
        Globals.declarations.append(".input "+name)
    else:
        Globals.declarations.append(dec_st)
        
    

def get_relation_name(name):
    if name in Globals.naming_dict:
        Globals.naming_dict[name]+=1
    else:
        Globals.naming_dict[name]=1
    return name + str(Globals.naming_dict[name])
