import numpy as np

class Cdh_rot:
    phi = 0
    alpha = 0
    a = 0
    d = 0
    stepSize = 1
    tran = np.array([])

    def __init__(self, _alpha, _a, _d, _initAngle, _stepSize):
        self.alpha = _alpha
        self.a = _a
        self.d = _d
        self.phi = _initAngle
        self.stepSize = _stepSize

        line1 = np.array([np.cos(np.radians(self.phi)), -np.sin(np.radians(self.phi))*np.cos(np.radians(self.alpha)), np.sin(np.radians(self.phi))*np.sin(np.radians(self.alpha)), self.a*np.cos(np.radians(self.phi))])
        line2 = np.array([np.sin(np.radians(self.phi)), np.cos(np.radians(self.phi)*np.cos(np.radians(self.alpha))), -np.cos(np.radians(self.phi))*np.sin(np.radians(self.alpha)),self.a*np.sin(np.radians(self.phi))])
        line3 = np.array([0, np.sin(np.radians(self.alpha)), np.cos(np.radians(self.alpha)), self.d])
        line4 = np.array([0,0,0,1])
        self.tran = np.array([line1, line2, line3, line4])
        print("Trans in Radians:")
        print(self.tran)

    def makeStep(self):
        self.phi = self.phi + 1 *self.stepSize
        line1 = np.array([np.cos(np.radians(self.phi)), -np.sin(np.radians(self.phi))*np.cos(np.radians(self.alpha)), np.sin(np.radians(self.phi))*np.sin(np.radians(self.alpha)), self.a*np.cos(np.radians(self.phi))])
        line2 = np.array([np.sin(np.radians(self.phi)), np.cos(np.radians(self.phi)*np.cos(np.radians(self.alpha))), -np.cos(np.radians(self.phi))*np.sin(np.radians(self.alpha)),self.a*np.sin(np.radians(self.phi))])
        line3 = np.array([0, np.sin(np.radians(self.alpha)), np.cos(np.radians(self.alpha)), self.d])
        line4 = np.array([0,0,0,1])
        self.tran = np.array([line1, line2, line3, line4])
    def getTrans(self):
        return self.tran

class Cdh_trans:
    phi = 0
    alpha = 0
    a = 0
    d = 0
    stepSize = 1
    tran = np.array([])

    def __init__(self, _phi,_alpha, _a, _initalLength, _stepSize):
        self.alpha = _alpha
        self.a = _a
        self.d = _initalLength
        self.phi = _phi
        self.stepSize = _stepSize

        line1 = np.array([np.cos(np.radians(self.phi)), -np.sin(np.radians(self.phi))*np.cos(np.radians(self.alpha)), np.sin(np.radians(self.phi))*np.sin(np.radians(self.alpha)), self.a*np.cos(np.radians(self.phi))])
        line2 = np.array([np.sin(np.radians(self.phi)), np.cos(np.radians(self.phi)*np.cos(np.radians(self.alpha))), -np.cos(np.radians(self.phi))*np.sin(np.radians(self.alpha)),self.a*np.sin(np.radians(self.phi))])
        line3 = np.array([0, np.sin(np.radians(self.alpha)), np.cos(np.radians(self.alpha)), self.d])
        line4 = np.array([0,0,0,1])
        self.tran = np.array([line1, line2, line3, line4])
        print("Trans in Radians:")
        print(self.tran)

    def makeStep(self):
        self.d = self.d + 1 *self.stepSize
        line1 = np.array([np.cos(np.radians(self.phi)), -np.sin(np.radians(self.phi))*np.cos(np.radians(self.alpha)), np.sin(np.radians(self.phi))*np.sin(np.radians(self.alpha)), self.a*np.cos(np.radians(self.phi))])
        line2 = np.array([np.sin(np.radians(self.phi)), np.cos(np.radians(self.phi)*np.cos(np.radians(self.alpha))), -np.cos(np.radians(self.phi))*np.sin(np.radians(self.alpha)),self.a*np.sin(np.radians(self.phi))])
        line3 = np.array([0, np.sin(np.radians(self.alpha)), np.cos(np.radians(self.alpha)), self.d])
        line4 = np.array([0,0,0,1])
        self.tran = np.array([line1, line2, line3, line4])
    def getTrans(self):
        return self.tran
    
_0t1 = Cdh_trans(90, -90, 200, 0, 1)
_1t2 = Cdh_rot(0, 2000, 0, 0, 5)
_2t3 = Cdh_rot(0, 1000, 0, 0, 5)
_3t4 = Cdh_rot(0, 500, 0, 0, 5)

_0t4 = _0t1.getTrans() * _1t2.getTrans() * _2t3.getTrans() * _3t4.getTrans()
print (_0t4)

testVec = np.matmul(_0t4, np.array([1, 1, 1, 1]))
print(testVec[:3])
