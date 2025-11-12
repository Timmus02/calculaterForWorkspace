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

    def __init__(self,_d, _a, _alpha, _stepSize, _max, _min):
        self.alpha = _alpha
        self.a = _a
        self.d = _d
        self.phi = _min
        self.stepSize = _stepSize
        self.max = _max
        self.min = _min
        self.__calcTrans()
        print("Trans:")
        print(self.tran)

    def __calcTrans(self):
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
            self.__calcTrans()
    def getTrans(self):
        return self.tran
    def setZero(self):
        self.phi = self.min
        self.__calcTrans()
    def setAngle(self, _angle):
        self.phi = _angle
        self.__calcTrans()

class Cdh_trans:
    phi = 0
    alpha = 0
    a = 0
    d = 0
    stepSize = 1
    tran = np.array([])
    max = 0
    min = 0

    def __init__(self, _phi, _a, _alpha, _stepSize, _max, _min):
        self.alpha = _alpha
        self.a = _a
        self.d = _min
        self.phi = _phi
        self.stepSize = _stepSize
        self.max = _max
        self.min = _min

        self.__calcTrans()
        print("Trans:")
        print(self.tran)

    def __calcTrans(self):
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
            self.__calcTrans()
    def getTrans(self):
        return self.tran
    def setZero(self):
        self.d = self.min
        self.__calcTrans()
    def setDist(self, _dist):
        self.d = _dist
        self.__calcTrans()