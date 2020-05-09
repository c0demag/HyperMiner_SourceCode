from BuildHorn import *

Users = [Variable("User", str(i)) for i in range(3) ]
Equalities = [Equality(i, random.sample([True, False], 1)[0]) for i in Users]
spec = Formula(AND(OR(F(Equalities[0]), G(Equalities[1])), X(Equalities[2])))
CreateHornClauses(spec, 0, True)