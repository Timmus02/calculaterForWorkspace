from sympy import symbols, Matrix, cos, sin, pprint
import classesDH as dh
import numpy as np
#Classe for DH
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
   
l2 = "l2"

l1 = 100
l3 = 600
l4 = 600
l5 = 600
l6 = 300

_0T1 = Cdh(0, l2, l1+l3, 0)
_1T2 = Cdh("-q1", 0, l4, 0)
_2T3 = Cdh("-q2", 0, l5, 0)
_3T4 = Cdh("-q3+90", 0, 0, 90)
_4T5 = Cdh("q4", l6, 0, 0)
_0T2 = _0T1.getTrans() * _1T2.getTrans()
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

JakobiTrans = Matrix([ [0 , 0 , 0, 0, 0],
                      [0 , 0 , 0, 0, 0],
                      [0 , 0 , 0, 0, 0]])
JakobiRot = Matrix([ [0 , 0 , 0, 0, 0],
                    [0 , 0 , 0, 0, 0],
                    [0 , 0 , 0, 0, 0]])
##calc 0rE

TCPVec = Matrix([0, 0, 0, 1])
_0rE = _0T5 * TCPVec

###########Achse2########################
_0r2 = _0T2.col(3) #4 Spalte
pprint(_0r2)
#_0r0 = Matrix([0], [0], [0], [1])
_0e2 = _0T1.getTrans().col(2) #3 Spalte
_0e2 = _0e2.row_del(3)
print(type(_0e2))
trans2 = _0e2.cross(_0rE.row_del(3) - _0r2.row_del(3)) #geht nur mit 3 Zeilen nicht 4
trans2 = trans2.col_join(Matrix([1]))
pprint(trans2)

Jakobi = Matrix([ JakobiTrans,
                  JakobiRot])
pprint(Jakobi)
###############Überprüfung der Nulllage###########################

#l2 = 0
#_0T1 = Cdh(0, l2, l1+l3, 0)
#_1T2 = Cdh(0, 0, l4, 0)
#_2T3 = Cdh(0, 0, l5, 0)
#_3T4 = Cdh(-90, 0, 0, 90)
#_4T5 = Cdh(0, l6, 0, 0)
#_0T5 = _0T1.getTrans() * _1T2.getTrans() * _2T3.getTrans() * _3T4.getTrans() * _4T5.getTrans()
#pprint(_0T5)

l1 = 100
l3 = 600
l4 = 600
l5 = 600
l6 = 300
_0t1 = dh.Cdh_trans(0,    l1+l3,    0,              200,     1,   0)
_1t2 = dh.Cdh_rot(0,        l4,      0,              10,     1,   0)
_2t3 = dh.Cdh_rot(0,        l5,      0,              10,     1,   0)
_3t4 = dh.Cdh_rot(0,         0,      90,             10,     1,   910) 
_4t5 = dh.Cdh_rot(l6,        0,      0,              0,      1,   0) #Endeffektor
_0t1.setZero()
_1t2.setZero()
_2t3.setZero()
_3t4.setZero()
_4t5.setZero()
_0t5 =_0t1.getTrans() @ _1t2.getTrans() @ _2t3.getTrans() @ _3t4.getTrans() @ _4t5.getTrans()
print(_0t5.round(2))