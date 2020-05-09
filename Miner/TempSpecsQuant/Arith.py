class Arithmetic(object):
    pass

class Equals(Arithmetic):
    def __init__(self, op1, op2):
        self.LHS = op1
        self.RHS = op2
    def __repr__(self):
        return str(self.LHS)+"="+str(self.RHS)

class NotEquals(Arithmetic):
    def __init__(self, op1, op2):
        self.LHS = op1
        self.RHS = op2
    def __repr__(self):
        return str(self.LHS)+"!="+str(self.RHS)

class Add(Arithmetic):
    def __init__(self, op1, op2):
        self.LHS = op1
        self.RHS = op2
    def __repr__(self):
        return str(self.LHS)+"+"+str(self.RHS)
    def evalaute(self):
        if isinstance(self.LHS, int) and isinstance(self.RHS, int):
            return self.LHS + self.RHS
        return str(self.LHS)+"+"+str(self.RHS)

class Sub(Arithmetic):
        def __init__(self, op1, op2):
            self.LHS = op1
            self.RHS = op2
        def __repr__(self):
            return str(self.LHS)+"-"+str(self.RHS)
        def evalaute(self):
            if isinstance(self.LHS, int) and isinstance(self.RHS, int):
                return self.LHS - self.RHS
            return str(self.LHS)+"-"+str(self.RHS)

class Compare(Arithmetic):
    def __init__(self, op1, op2, rel=1):        # 0 for smaller, 1 for greater, 2 for smaller and equal, 3 for greater and equal
        self.LHS = op1
        self.RHS = op2
        self.Rel = rel
    def __repr__(self):
        if self.Rel==0:
            return str(self.LHS)+"<"+str(self.RHS)
        if self.Rel==1:
            return str(self.LHS)+">"+str(self.RHS)
        if self.Rel==2:
            return str(self.LHS)+"<="+str(self.RHS)
        return str(self.LHS)+">="+str(self.RHS)
    def evalaute(self):
        if isinstance(self.LHS, int) and isinstance(self.RHS, int):
            if self.Rel==0:
                return self.LHS < self.RHS
            if self.Rel==1:
                return self.LHS > self.RHS
            if self.Rel==2:
                return self.LHS <= self.RHS
            return self.LHS >= self.RHS
        if self.Rel==0:
            return str(self.LHS)+"<"+str(self.RHS)
        if self.Rel==1:
            return str(self.LHS)+">"+str(self.RHS)
        if self.Rel==2:
            return str(self.LHS)+"<="+str(self.RHS)
        return str(self.LHS)+">="+str(self.RHS)

def GT(a, b):
    return Compare(a, b, 1)

def LT(a, b):
    return Compare(a, b, 0)

def LE(a, b):
    return Compare(a, b, 2)

def GE(a, b):
    return Compare(a, b, 3)