import numpy as np
class Cdh_rot:
    phi = 0
    alpha = 0
    a = 0
    d = 0
    stepSize = 1
    tran = np.array([])
    min = 0
    max = 360

    def __init__(self, _alpha, _a, _d, _initAngle, _stepSize, _max, _min):
        self.alpha = _alpha
        self.a = _a
        self.d = _d
        self.phi = _initAngle
        self.stepSize = _stepSize
        self.max = _max
        self.min = _min
        self.calcTrans()
        print("Trans:")
        print(self.tran)

    def calcTrans(self):
        phi = np.radians(self.phi)
        alpha = np.radians(self.alpha)
        self.tran = np.array([
            [np.cos(phi), -np.sin(phi)*np.cos(alpha),  np.sin(phi)*np.sin(alpha), self.a*np.cos(phi)],
            [np.sin(phi),  np.cos(phi)*np.cos(alpha), -np.cos(phi)*np.sin(alpha), self.a*np.sin(phi)],
            [0,            np.sin(alpha),              np.cos(alpha),              self.d],
            [0,            0,                          0,                          1]
        ])

    def makeStep(self):
        self.phi = self.phi + 1 *self.stepSize
        if self.phi < self.max:
            self.calcTrans()
    def getTrans(self):
        return self.tran
    def getStepSize(self):
        return self.stepSize
    def setZero(self):
        self.phi = self.min
        self.calcTrans()

class Cdh_trans:
    phi = 0
    alpha = 0
    a = 0
    d = 0
    stepSize = 1
    tran = np.array([])
    max = 0
    min = 0

    def __init__(self, _phi,_alpha, _a, _initalLength, _stepSize, _max, _min):
        self.alpha = _alpha
        self.a = _a
        self.d = _initalLength
        self.phi = _phi
        self.stepSize = _stepSize
        self.max = _max
        self.min = _min

        self.calcTrans()
        print("Trans:")
        print(self.tran)

    def calcTrans(self):
        phi = np.radians(self.phi)
        alpha = np.radians(self.alpha)
        self.tran = np.array([
            [np.cos(phi), -np.sin(phi)*np.cos(alpha),  np.sin(phi)*np.sin(alpha), self.a*np.cos(phi)],
            [np.sin(phi),  np.cos(phi)*np.cos(alpha), -np.cos(phi)*np.sin(alpha), self.a*np.sin(phi)],
            [0,            np.sin(alpha),              np.cos(alpha),              self.d],
            [0,            0,                          0,                          1]
        ])

    def makeStep(self):
        self.d = self.d + 1 *self.stepSize
        if self.d < self.max:
            self.calcTrans()
    def getTrans(self):
        return self.tran
    def getStepSize(self):
        return self.stepSize
    def setZero(self):
        self.d = self.min
        self.calcTrans()