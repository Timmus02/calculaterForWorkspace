from sympy import symbols, Matrix, cos, sin, pprint

class Cdh:
    phi = 0
    alpha = 0
    a = 0
    d = 0
    phi, d, a, alpha = symbols('phi d a alpha')

    def __init__(self, _phi, _d, _a, _alpha):
        self.alpha = _alpha
        self.a = _a
        self.d = _d
        self.phi = _phi
        self.__calcTrans()
        #print("Trans:")
        #print(self.tran)

    def __calcTrans(self):
        phi, alpha, a, d = self.phi, self.alpha, self.a, self.d
        self.tran = Matrix([
            [cos(phi), -sin(phi)*cos(alpha),  sin(phi)*sin(alpha),  a*cos(phi)],
            [sin(phi),  cos(phi)*cos(alpha), -cos(phi)*sin(alpha),  a*sin(phi)],
            [0,         sin(alpha),           cos(alpha),           d],
            [0,         0,                    0,                    1]
        ])    
    def getTrans(self):
        return self.tran
   
l1 = 5
l2 = "l2"
l3 = 15
l4 = 4
l5 = 2
l6 = 8

_0T1 = Cdh(0, l2, l1+l3, 0)
_1T2 = Cdh("-q1", 0, l4, 0)
_2T3 = Cdh("-q2", 0, l5, 0)
_3T4 = Cdh("-q3+90", 0, 0, 90)
_4T5 = Cdh("q4", l6, 0, 0)
_0T5 = _0T1.getTrans() * _1T2.getTrans() * _2T3.getTrans() * _3T4.getTrans() * _4T5.getTrans()

print("######0T1#########")
pprint(_0T1.getTrans())
print("######1T2######")
pprint(_1T2.getTrans())

print("######2T3######")
pprint(_2T3.getTrans())
print("######3T4######")
pprint(_3T4.getTrans())
print("######4T5######")
pprint(_4T5.getTrans())

print("######0T5######")
pprint(_0T5)

for row in _0T5.tolist():
            formatted = [str(item) for item in row]
            print("  ".join(formatted))
with open("_0T5.txt", "w") as dill_file:
    for row in _0T5.tolist():
        formatted = [str(item) for item in row]
        dill_file.write(str(" | ".join(formatted)))
        dill_file.write("\n")
    