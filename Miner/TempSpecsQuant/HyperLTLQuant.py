# coding: utf-8

import copy
import os, sys
from ClauseAST import *
from Arith import *
import Globals
import random



class TempSpecs(object):
    def __init__(self, quant):
        self.cl = "TempSpec"
        self.QuantFormula = quant
    def __repr__(self):
        return str(self.QuantFormula)
    def __eq__(self, ob):
        return hasattr(ob, 'cl') and self.cl == ob.cl and self.QuantFormula == ob.QuantFormula
    def __hash__(self):
        return hash((self.cl, self.QuantFormula))
    def negate(self):
        ob = copy.deepcopy(self)
        return TempSpecs(ob.QuantFormula.negate())
    def holes(self):
        return self.QuantFormula.holes()
    def fill_hole(self, arg):
        return self.QuantFormula.fill_hole(arg)
    def depth(self):
        return self.QuantFormula.depth()
    def build_horn(self, approach, isFormula = False):
        clause, TL = self.QuantFormula.build_horn(approach, isFormula)
        mod_clause_head = copy.deepcopy(clause.Head)
        mod_clause_head.Vars[0] = "0"
        clause_head = Relation("TempSpec", ["Result"])
        clause_body = Body([Equals("Result", "0"), mod_clause_head])
        T_Clause = Clause(clause_head, clause_body)
        Globals.rules.append(T_Clause)
        Globals.rules.append("\n")
        declarer("TempSpec", len(clause_head.Vars))
        Globals.declarations.append(".output TempSpec")
        return T_Clause, TL

class Quantifier(TempSpecs):
    def __init__(self, cl, trace, formula):
        self.cl = cl
        self.Trace = trace
        self.Formula = formula
    def __repr__(self):
        return str(self.cl) + " " + str(self.Trace) + ", " + str(self.Formula)
    def holes(self):
        return self.Formula.holes()
    def __eq__(self, ob):
        return hasattr(ob, 'cl') and self.cl == ob.cl and self.Trace == ob.Trace and self.Formula == ob.Formula
    def __hash__(self):
        return hash((self.cl, self.Trace, self.Formula))
    def fill_hole(self, arg):
        return self.Formula.fill_hole(arg)
    def depth(self):
        return self.Formula.depth()
    
class ForAll(Quantifier):
    def __init__(self, trace, formula):
        super().__init__("ForAll", trace, formula)
    def negate(self):
        ob = copy.deepcopy(self)
        return Exists(ob.Trace, ob.Formula.negate())
    def build_horn(self, approach, isFormula = False):
        head = get_relation_name(self.cl)
        
        rec_clause, TL = self.Formula.build_horn(approach, isFormula)
        
        Current_clause_head = Relation(head, copy.deepcopy(rec_clause.Head.Vars))

        if rec_clause.Head.Vars[-1] == "0":
            Current_clause_head.Vars = Current_clause_head.Vars[:-1]
        
        next_it_head = copy.deepcopy(Current_clause_head)
        next_it_head.Vars[-1] = Add(next_it_head.Vars[-1], 1)
        
        Trace_Var = Variable("Tr", self.Trace)
        clause_body_iterative = Body([Compare(Trace_Var, 0, 3), Compare(Trace_Var, "max MaxTrace : TraceEnd(MaxTrace, _)", 0), rec_clause.Head, next_it_head])
        clause_body_terminate = Body([Equals(Trace_Var, "max MaxTrace : TraceEnd(MaxTrace, _)"), rec_clause.Head])

        clause_iterate = Clause(Current_clause_head, clause_body_iterative)
        clause_terminate = Clause(Current_clause_head, clause_body_terminate)

        declarer(head, len(Current_clause_head.Vars))
        Globals.rules.append(clause_iterate)
        Globals.rules.append(clause_terminate)
        Globals.rules.append("\n")
        
        clause = copy.deepcopy(clause_iterate)
        clause.Head.Vars[-1] = "0"

        return clause, TL


class Exists(Quantifier):
    def __init__(self, trace, formula):
        super().__init__("Exists", trace, formula)
    def negate(self):
        ob = copy.deepcopy(self)
        return ForAll(ob.Trace, ob.Formula.negate())
    def build_horn(self, approach, isFormula = False):
        head = get_relation_name(self.cl)
        
        rec_clause, TL = self.Formula.build_horn(approach, isFormula)
        
        Current_clause_head = Relation(head, copy.deepcopy(rec_clause.Head.Vars))

        if rec_clause.Head.Vars[-1] == "0":
            Current_clause_head.Vars = Current_clause_head.Vars[:-1]
        
        tmpvar = Variable("Tmp", "")
        next_it_head = copy.deepcopy(Current_clause_head)
        next_it_head.Vars[-1] = tmpvar
        

        Trace_Var = Variable("Tr", self.Trace)
        
        InEqList = []
        for i in Current_clause_head.Vars[1: -1]:
            InEqList.append(NotEquals(Trace_Var, i))

        clause_body_iterative = Body([Compare(Trace_Var, 0, 3), Compare(Trace_Var, "max MaxTrace : TraceEnd(MaxTrace, _)", 2), Equals(Trace_Var, Sub(tmpvar, 1)), next_it_head])
        clause_body_terminate = Body([Compare(Trace_Var, 0, 3), Compare(Trace_Var, "max MaxTrace : TraceEnd(MaxTrace, _)", 2), rec_clause.Head]+InEqList)

        clause_iterate = Clause(Current_clause_head, clause_body_iterative)
        clause_terminate = Clause(Current_clause_head, clause_body_terminate)

        declarer(head, len(Current_clause_head.Vars))
        Globals.rules.append(clause_iterate)
        Globals.rules.append(clause_terminate)
        Globals.rules.append("\n")
        
        clause = copy.deepcopy(clause_iterate)
        clause.Head.Vars[-1] = "0"

        return clause, TL



class Formula(TempSpecs):
    def __init__(self, spec):
        self.cl = "Formula"
        self.Spec = spec
        
    def __repr__(self):
        return str(self.Spec)

    def negate(self):
        ob = copy.deepcopy(self)
        return Formula(ob.Spec.negate())

    def build_horn(self, approach, isFormula = False):
        clause, TL = self.Spec.build_horn(approach, isFormula)
        if isFormula:
            head = get_relation_name(self.cl)
            Args = copy.deepcopy(clause.Head.Vars)[1:]
            mod_clause_head = copy.deepcopy(clause.Head)
            mod_clause_head.Vars[0] = "0"
            new_clause = Clause(Relation(head, Args), Body([mod_clause_head]))
            declarer(head, len(Args))
            Globals.rules.append(new_clause)
            Globals.declarations.append(".output " + str(head))
            return new_clause, TL

        return clause, TL

    def holes(self):
        return self.Spec.holes()

    def __eq__(self, ob):
        return hasattr(ob, 'cl') and self.cl==ob.cl and self.Spec==ob.Spec
    
    def __hash__(self):
        return hash((self.cl, self.Spec))

    def fill_hole(self, arg):
        return self.Spec.fill_hole(arg)
        
    def depth(self):
        return self.Spec.depth()

class Variable(TempSpecs):

    def __init__(self, name, tr):
        self.cl="Variable"
        self.Name = name
        self.Trace = tr
    
    def __repr__(self):
        return str(self.Name)+str(self.Trace)
    
    def __eq__(self, ob):
        return hasattr(ob, 'cl') and self.cl == ob.cl and self.Name == ob.Name and self.Trace == ob.Trace
    
    def __hash__(self):
        return hash((self.cl, self.Name, self.Trace))
    
    def negate(self):
        tmp = copy.deepcopy(self)
        return tmp
    
    def fill_hole(self, arg):
        return -1
    
    def build_horn(self, approach, isFormula = False):
        sys.exit("Must not be here, must use Equality to introduce variables in the Formula.")
    
    def holes(self):
        return False
    
    def depth(self):
        return 1

class Hole(TempSpecs):
    def __init__(self):
        self.cl = "Hole"
    def __repr__(self):
        return "_"
    def __eq__(self, ob):
        return self.cl == ob.cl
    def __hash__(self):
        return hash((self.cl))
    def holes(self):
        return True
    def depth(self):
        return 0
    def fill_hole(self, arg):
        return -1
    def negate(self):
        sys.exit("Can't negate an Incomplete Specification")
    def build_horn(self, approach, isFormula = False):
        sys.exit("Can't build Horn Clause for an Incomplete Specification")

class Operators(object):
    pass

class BinaryOperators(Operators):
    def __init__(self, cl, lhs, rhs):
        self.cl = cl
        self.LHS = lhs
        self.RHS = rhs
    def holes(self):
        if isinstance(self.RHS, int) or isinstance(self.RHS, bool):
            return self.LHS.holes() 
        return self.LHS.holes() or self.RHS.holes()
    def __eq__(self, ob):
        return hasattr(ob, 'cl') and self.cl == ob.cl and ((self.RHS==ob.RHS and self.LHS==ob.LHS) or (self.RHS==ob.LHS and self.LHS==ob.RHS))
    def __hash__(self):
        return hash((self.cl, self.LHS, self.RHS))
    def fill_hole(self, arg):
        x = 1
        if type(self.LHS)==type(Hole()):
            self.LHS=arg
        elif type(self.RHS)==type(Hole()):
            self.RHS=arg
        elif self.LHS.holes():
            x = self.LHS.fill_hole(arg)
        elif hasattr(self.RHS, 'cl') and self.RHS.holes():
            x =  self.RHS.fill_hole(arg)
        else:
            return -1
        if self.LHS == self.RHS or x == -1:
                return -1
        return 1
    def depth(self):
        if isinstance(self.RHS, int) or isinstance(self.RHS, bool):
            return 1 + self.LHS.depth()
        return 1+max(self.LHS.depth(), self.RHS.depth())



class Equality(BinaryOperators):
    def __init__(self, lhs, rhs):
        super().__init__("Equality", lhs, rhs)
    def __repr__(self):            
        if isinstance(self.RHS, bool):
            if self.RHS:
                return str(self.LHS)
            return "!"+str(self.LHS)
        return "(" + str(self.LHS) + "==" + str(self.RHS)+")" 

    def negate(self):
        ob = copy.deepcopy(self)
        if ob.RHS in [True, False]:
            ob.RHS = not ob.RHS
            return ob
        return InEquality(ob.LHS, ob.RHS)        

    def build_horn(self, approach, isFormula = False):
        head = get_relation_name(self.cl)
        Globals.magic_transform.add(head)

        Var1, Var2 = copy.deepcopy(self.LHS), copy.deepcopy(self.RHS)
        TL1, TL2 = [], []

        assert hasattr(Var1, 'cl') and Var1.cl == "Variable"
        assert (hasattr(Var2, 'cl') and Var2.cl == "Variable") or (Var2 in [True, False])

        LTrace = Var1.Trace
        LName = Var1.Name
        TL1.append(LTrace)
        if LName not in Globals.declared.keys():
            declarer(LName, 3, True)            # 3 because trace contains 3 objects Trace, Time, Value
            Globals.declared[LName] = "1"

        if Var2 in [True, False]:
            clause_body = Body([Relation(LName, [TraceVariable(LTrace), T, "1" if Var2 else "0"]), LE(T, TE), CommonEnd(TE)])
        else:
            Output_Var = Variable("Out", "")
            RTrace = Var2.Trace
            RName = Var2.Name
            TL2.append(Var2.Trace)
            if RName not in Globals.declared.keys():
                declarer(RName, 3, True)            # 3 because trace contains 3 objects Trace, Time, Value
                Globals.declared[RName] = "1"
            
            InEq_Clause = [NotEquals(TraceVariable(LTrace), TraceVariable(RTrace))]

            clause_body = Body([Relation(LName, [TraceVariable(LTrace), T, Output_Var]), Relation(RName, [TraceVariable(RTrace), T, Output_Var])]+InEq_Clause + [LE(T, TE), CommonEnd(TE)])
        
        Trace_List = list(set(TL1+TL2))
        Trace_List.sort()

        Args = [T] + [TraceVariable(i) for i in Trace_List]

        clause_head = Relation(head, Args)
        clause = Clause(clause_head, clause_body)
        Globals.rules.append(clause)
        Globals.rules.append("\n")
        declarer(head, len(clause_head.Vars))

        return clause, Trace_List
            
        


class InEquality(BinaryOperators):
    def __init__(self, lhs, rhs):
        super().__init__("InEquality", lhs, rhs)
    def __repr__(self):
        if isinstance(self.RHS, bool):
            if not self.RHS:
                return str(self.LHS)
            return "!"+str(self.LHS)
        return "(" + str(self.LHS) + "!=" + str(self.RHS)+")"
    def negate(self):
        ob = copy.deepcopy(self)
        return Equality(ob.LHS, ob.RHS)

    def build_horn(self, approach, isFormula = False):
        head = get_relation_name(self.cl)
        Globals.magic_transform.add(head)

        Var1, Var2 = copy.deepcopy(self.LHS), copy.deepcopy(self.RHS)
        TL1, TL2 = [], []

        assert hasattr(Var1, 'cl') and Var1.cl == "Variable"
        assert (hasattr(Var2, 'cl') and Var2.cl == "Variable") or (Var2 in [True, False])

        LTrace = Var1.Trace
        LName = Var1.Name
        TL1.append(LTrace)
        if LName not in Globals.declared.keys():
            declarer(LName, 3, True)            # 3 because trace contains 3 objects Trace, Time, Value
            Globals.declared[LName] = "1"

        if Var2 in [True, False]:
            clause_body = Body([Relation(LName, [TraceVariable(LTrace), T, "0" if Var2 else "1"]), LE(T, TE), CommonEnd(TE)])
        else:
            Output_Var1 = Variable("Out", "1")
            Output_Var2 = Variable("Out", "2")
            RTrace = Var2.Trace
            RName = Var2.Name
            TL2.append(Var2.Trace)
            if RName not in Globals.declared.keys():
                declarer(RName, 3, True)            # 3 because trace contains 3 objects Trace, Time, Value
                Globals.declared[RName] = "1"

            InEq_Clause = [NotEquals(TraceVariable(LTrace), TraceVariable(RTrace))]

            clause_body = Body([Relation(LName, [TraceVariable(LTrace), T, Output_Var1]), Relation(RName, [TraceVariable(RTrace), T, Output_Var2]), NotEquals(Output_Var1, Output_Var2)]+InEq_Clause+[LE(T, TE), CommonEnd(TE)])
        
        Trace_List = list(set(TL1+TL2))
        Trace_List.sort()

        Args = [T] + [TraceVariable(i) for i in Trace_List]

        clause_head = Relation(head, Args)
        clause = Clause(clause_head, clause_body)
        Globals.rules.append(clause)
        Globals.rules.append("\n")
        declarer(head, len(clause_head.Vars))

        return clause, Trace_List


class AND(BinaryOperators):
    def __init__(self, lhs, rhs, WasImplication = False):
        super().__init__("AND", lhs, rhs)
        self.WasImplication = WasImplication
    def __repr__(self):
        return "("+str(self.LHS)+ " & " +str(self.RHS)+")"
    def negate(self):
        ob = copy.deepcopy(self)
        return OR(ob.LHS.negate(), ob.RHS.negate())

    def build_horn(self, approach, isFormula = False):
        head = get_relation_name(self.cl)
        Globals.magic_transform.add(head)

        r1, TL1 = None, None
        if self.WasImplication == True:
            r1, TL1 = self.LHS.build_horn((1+approach)%2, isFormula)
        else:
            r1, TL1 = self.LHS.build_horn(approach, isFormula)
        r2, TL2 = self.RHS.build_horn(approach, isFormula)

        if TL1 != TL2:
            Trace_List = list(set(TL1 + TL2))
            Trace_List.sort()
            rel_args = [T] + [Variable("Tr", i) for i in Trace_List]
        else:
            Trace_List = TL1
            Trace_List.sort()
            rel_args = copy.deepcopy(r1.Head.Vars)

        declarer(head, len(rel_args))

        InEq_Clause = []
        for i in Trace_List:
            for j in Trace_List:
                if i<j:
                    InEq_Clause.append(NotEquals(TraceVariable(i), TraceVariable(j)))

        clause = Clause(Relation(head, rel_args), Body([r1.Head, r2.Head]+InEq_Clause))
        Globals.rules.append(clause)
        Globals.rules.append("\n")

        return clause, Trace_List

class OR(BinaryOperators):
    def __init__(self, lhs, rhs):
        super().__init__("OR", lhs, rhs)
    def __repr__(self):
        return "(" + str(self.LHS)+ " | " +str(self.RHS) + ")"
    def negate(self):
        ob = copy.deepcopy(self)
        return AND(ob.LHS.negate(), ob.RHS.negate())

    def build_horn(self, approach, isFormula = False):
        head = get_relation_name(self.cl)
        Globals.magic_transform.add(head)

        r1, TL1 = self.LHS.build_horn(approach, isFormula)
        r2, TL2 = self.RHS.build_horn(approach, isFormula)

        Tr_End_LeftOut_First = []        # TraceEnds for the traces that are left out for the 
        Tr_End_LeftOut_Sec = [] 
        if TL1 != TL2:
            Trace_List = list(set(TL1 + TL2))
            Trace_List.sort()
            rel_args = [T] + [TraceVariable(i) for i in Trace_List]
            for i in Trace_List:
                if i not in TL1:
                    Tr_End_LeftOut_First.append(TraceEnd(i, Hole()))
                if i not in TL2:
                    Tr_End_LeftOut_Sec.append(TraceEnd(i, Hole()))
        else:
            Trace_List = TL1
            Trace_List.sort()
            rel_args = copy.deepcopy(r1.Head.Vars)

        declarer(head, len(rel_args))

        InEq_Clause = []
        for i in Trace_List:
            for j in Trace_List:
                if i<j:
                    InEq_Clause.append(NotEquals(TraceVariable(i), TraceVariable(j)))

        clause_first = Clause(Relation(head, rel_args), Body([r1.Head]+Tr_End_LeftOut_First+InEq_Clause))
        clause_second = Clause(Relation(head, rel_args), Body([r2.Head]+Tr_End_LeftOut_Sec+InEq_Clause))
        Globals.rules.append(clause_first)
        Globals.rules.append(clause_second)
        Globals.rules.append("\n")
        
        return clause_first, Trace_List

class UnaryOperators(Operators):
    def __init__(self, cl, expr):
        self.cl = cl
        self.RHS = expr
    def holes(self):
        return self.RHS.holes()
    def __eq__(self, ob):
        return hasattr(ob, 'cl') and self.cl == ob.cl and self.RHS==ob.RHS
    def __hash__(self):
        return hash((self.cl, self.RHS))
    def fill_hole(self, arg):
        if type(self.RHS)==type(Hole()):
            self.RHS=arg
        elif self.RHS.holes():
            return self.RHS.fill_hole(arg)
        else:
            return -1
        return 1
    def depth(self):
        return 1+self.RHS.depth()

class NOT(UnaryOperators):
    def __init__(self, rhs):
        super().__init__("NOT", rhs)
    def __repr__(self):
        return "!("+str(self.RHS)+")"
    def negate(self):
        ob = copy.deepcopy(self)
        return ob.RHS
    def build_horn(self, approach, isFormula = False):
        New_f = self.RHS.negate()
        return New_f.build_horn(approach, isFormula)


class G(UnaryOperators):
    def __init__(self, rhs):
        super().__init__("G", rhs)

    def __repr__(self):
        return "G("+str(self.RHS)+")"

    def negate(self):
        ob = copy.deepcopy(self)
        return F(ob.RHS.negate())

    def build_horn(self, approach, isFormula = False):
        head = get_relation_name(self.cl)
        Globals.magic_transform.add(head)

        rel, Trace_List = self.RHS.build_horn(approach, isFormula)
        Trace_List.sort()

        body_list = [GE(T, 0), CommonEnd(TE)]

        Args = [T] + [TraceVariable(i) for i in Trace_List]
        
        declarer(head, len(Args))

        Current_Iteration_Head = Relation(head, Args)
        Next_Iteration_Head = copy.deepcopy(Current_Iteration_Head)
        Next_Iteration_Head.Vars[0] = Add(T, 1)

        if approach == 1:       # Optimistic
            body_list.append(LT(T, TE))
            Clause_Terminate = Clause(Current_Iteration_Head, Body([CommonEnd(T), rel.Head]))
            Globals.rules.append(Clause_Terminate)
        else:
            body_list.append(LE(T, TE))

        body_list.append(Next_Iteration_Head)
        body_list.append(rel.Head) 
        Clause_Iterative = Clause(Current_Iteration_Head, Body(body_list))
        Globals.rules.append(Clause_Iterative)
        Globals.rules.append("\n")
        
        return Clause_Iterative, Trace_List
        


class F(UnaryOperators):
    def __init__(self, rhs):
        super().__init__("F", rhs)

    def __repr__(self):
        return "F("+str(self.RHS)+")"

    def negate(self):
        ob = copy.deepcopy(self)
        return G(ob.RHS.negate())

    def build_horn(self, approach, isFormula = False):
        head = get_relation_name(self.cl)
        Globals.magic_transform.add(head)

        rel, Trace_List = self.RHS.build_horn(approach, isFormula)
        Trace_List.sort()

        body_list = [GE(T, 0), CommonEnd(TE), LT(T, TE), Equals(T, Sub(T1, 1))]

        Args = [T] + [TraceVariable(i) for i in Trace_List]
        
        declarer(head, len(Args))

        Current_Iteration_Head = Relation(head, Args)
        Next_Iteration_Head = copy.deepcopy(Current_Iteration_Head)
        Next_Iteration_Head.Vars[0] = T1
        
        body_list.append(Next_Iteration_Head)

        if approach == 1:       # Optimistic
            TEnds = [TraceEnd(i, T) for i in Trace_List]
            InEq_Clause = []
            for i in Trace_List:
                for j in Trace_List:
                    if i<j:
                        InEq_Clause.append(NotEquals(TraceVariable(i), TraceVariable(j)))
            Clause_All = Clause(Current_Iteration_Head, Body(TEnds+InEq_Clause))
            Globals.rules.append(Clause_All)

        Clause_Terminate = Clause(Current_Iteration_Head, Body([rel.Head]))
        Globals.rules.append(Clause_Terminate)
        Clause_Iterative = Clause(Current_Iteration_Head, Body(body_list))
        Globals.rules.append(Clause_Iterative)
        Globals.rules.append("\n")
        
        return Clause_Iterative, Trace_List


    
class X(UnaryOperators):
    def __init__(self, rhs):
        super().__init__("X", rhs)

    def __repr__(self):
        return "X("+str(self.RHS)+")"

    def negate(self):
        ob = copy.deepcopy(self)
        return X(ob.RHS.negate())

    def build_horn(self, approach, isFormula = False):
        head = get_relation_name(self.cl)
        Globals.magic_transform.add(head)

        rel, Trace_List = self.RHS.build_horn(approach, isFormula)
        Trace_List.sort()

        body_list = [GE(T, 0), CommonEnd(TE), LT(T, TE), Equals(T, Sub(T1, 1))]

        Args = [T] + [TraceVariable(i) for i in Trace_List]
        
        declarer(head, len(Args))

        Current_Iteration_Head = Relation(head, Args)
        Next_Iteration_RelHead = copy.deepcopy(rel.Head)
        Next_Iteration_RelHead.Vars[0] = T1
        
        body_list.append(Next_Iteration_RelHead)

        if approach == 1:       # Optimistic
            TEnds = [TraceEnd(i, T) for i in Trace_List]
            InEq_Clause = []
            for i in Trace_List:
                for j in Trace_List:
                    if i<j:
                        InEq_Clause.append(NotEquals(TraceVariable(i), TraceVariable(j)))
            Clause_All = Clause(Current_Iteration_Head, Body(TEnds+InEq_Clause))
            Globals.rules.append(Clause_All)


        Clause_Iterative = Clause(Current_Iteration_Head, Body(body_list))
        Globals.rules.append(Clause_Iterative)
        Globals.rules.append("\n")
        
        return Clause_Iterative, Trace_List

        


class Implies(BinaryOperators):
    def __init__(self, lhs, rhs):
        super().__init__("Implies", lhs, rhs)
    def __repr__(self):
        return "(" + str(self.LHS)+ " => " +str(self.RHS) + ")"

    def negate(self):
        ob = copy.deepcopy(self)
        return AND(ob.LHS, ob.RHS.negate(), True)

    def build_horn(self, approach, isFormula = False):
        head = get_relation_name(self.cl)
        Globals.magic_transform.add(head)

        new_LHS = copy.deepcopy(self.LHS.negate())

        r1, TL1 = new_LHS.build_horn((1+approach)%2, isFormula)
        r2, TL2 = self.RHS.build_horn(approach, isFormula)

        Tr_End_LeftOut_First = []        # TraceEnds for the traces that are left out for the 
        Tr_End_LeftOut_Sec = [] 
        if TL1 != TL2:
            Trace_List = list(set(TL1 + TL2))
            Trace_List.sort()
            rel_args = [T] + [TraceVariable(i) for i in Trace_List]
            for i in Trace_List:
                if i not in TL1:
                    Tr_End_LeftOut_First.append(TraceEnd(i, Hole()))
                if i not in TL2:
                    Tr_End_LeftOut_Sec.append(TraceEnd(i, Hole()))
        else:
            Trace_List = TL1
            Trace_List.sort()
            rel_args = copy.deepcopy(r1.Head.Vars)

        declarer(head, len(rel_args))

        InEq_Clause = []
        for i in Trace_List:
            for j in Trace_List:
                if i<j:
                    InEq_Clause.append(NotEquals(TraceVariable(i), TraceVariable(j)))

        clause_first = Clause(Relation(head, rel_args), Body([r1.Head]+Tr_End_LeftOut_First+InEq_Clause))
        clause_second = Clause(Relation(head, rel_args), Body([r2.Head]+Tr_End_LeftOut_Sec+InEq_Clause))
        Globals.rules.append(clause_first)
        Globals.rules.append(clause_second)
        Globals.rules.append("\n")
        
        return clause_first, Trace_List


class BiImplies(BinaryOperators):
    def __init__(self, lhs, rhs):
        super().__init__("Bi-Implies", lhs, rhs)
    def __repr__(self):
        return "(" + str(self.LHS)+ " <==> " +str(self.RHS) + ")"

    def negate(self):
        ob = copy.deepcopy(self)
        ob = copy.deepcopy(AND(Implies(ob.LHS, ob.RHS), Implies(ob.RHS, ob.LHS)))
        return ob.negate()

    def build_horn(self, approach, isFormula = False):
        ob = copy.deepcopy(self)
        New_f = copy.deepcopy(AND(Implies(ob.LHS, ob.RHS), Implies(ob.RHS, ob.LHS)))
        return New_f.build_horn(approach, isFormula)


def ConvertToNNF(formula):
    formula_tmp = copy.deepcopy(formula)
    if formula_tmp.cl == "TempSpec":
        formula_tmp.QuantFormula = ConvertToNNF(formula_tmp.QuantFormula)
    elif formula_tmp.cl in ["ForAll", "Exists"]:
        formula_tmp.Formula = ConvertToNNF(formula_tmp.Formula)
    elif formula_tmp.cl == "Formula":
        formula_tmp.Spec = ConvertToNNF(formula_tmp.Spec)
    elif formula_tmp.cl == "NOT":
        formula_tmp=formula_tmp.negate()
        formula_tmp=formula_tmp.negate()
    elif formula_tmp.cl in ["AND", "OR", "Equality", "InEquality", "Implies"]:
        formula_tmp.LHS = ConvertToNNF(formula_tmp.LHS)
        if not isinstance(formula_tmp.RHS, int):
            formula_tmp.RHS = ConvertToNNF(formula_tmp.RHS)
    elif formula_tmp.cl == "Bi-Implies":
        formula_tmp = ConvertToNNF(AND(Implies(formula_tmp.LHS, formula_tmp.RHS), Implies(formula_tmp.RHS, formula_tmp.LHS)))
    elif formula_tmp.cl in ["G", "F", "X"]:
        formula_tmp.RHS = ConvertToNNF(formula_tmp.RHS)
    return formula_tmp


def CommonEnd(Var):
    return Relation("CommonEnd", [Var])
def TraceEnd(TrVar, TVar):
    return Relation("TraceEnd", [TraceVariable(TrVar), TVar])
def TraceVariable(Var):
    return Variable("Tr", str(Var))
def TimeVariable(Var):
    return Variable("T"+str(Var), "")

T = TimeVariable("")
T1 = TimeVariable("1")
TE = TimeVariable("E")
