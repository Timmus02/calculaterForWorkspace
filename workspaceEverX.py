import numpy as np
import open3d as o3d
import classesDH as dh
from rich.progress import Progress 
import time 
import csv

def calc(_save, _file):
    #minima maxima aus Kuka KR120R2700 ohne jeden Grund --> Ähnlicher Aufbau nur A2;A3;A5
    #                   _phi,_alpha, _a, _initalLength, _stepSize, _max, _min
    _0t1 = dh.Cdh_trans(90, 0, 200, 0, 20, 20000, 0)
    #                 _alpha, _a, _d, _initAngle, _stepSize, _max, _min
    _1t2 = dh.Cdh_rot(0, 200, 0, 0, 10, -5, -140)
    _2t3 = dh.Cdh_rot(0, 100, 0, 0, 10, 168, -120)
    _3t4 = dh.Cdh_rot(0, 50, 0, 0, 10, 125, -125) 
    _4t5 = dh.Cdh_rot(-90, 50, 0, 90, 0, 0, 0) #Endeffektor

    _total = _0t1.max/_0t1.stepSize * int((abs(_1t2.min) +abs(_1t2.max))/_1t2.stepSize) * int((abs(_2t3.min) +abs(_2t3.max))/_2t3.stepSize) * int((abs(_3t4.min) +abs(_3t4.max))/_3t4.stepSize)
    print(_total)
    time.sleep(1)
    with Progress() as p: #Progressbar
        t = p.add_task("Processing...", total=_total)
        while not p.finished:
            points = []
            step1 = 0
            _0t1.setZero()
            while step1 < _0t1.max/_0t1.stepSize:
                _0t1.makeStep()
                step1 += _0t1.stepSize

                _1t2.setZero()
                for i in range(int((abs(_1t2.min) +abs(_1t2.max))/_1t2.stepSize)):
                    _1t2.makeStep()

                    _2t3.setZero()
                    for i in range(int((abs(_2t3.min) +abs(_2t3.max))/_2t3.stepSize)):
                        _2t3.makeStep()

                        _3t4.setZero()
                        for i in range(int((abs(_3t4.min) +abs(_3t4.max))/_3t4.stepSize)):
                            _3t4.makeStep()
                            _0t4 = _0t1.getTrans() @ _1t2.getTrans() @ _2t3.getTrans() @ _3t4.getTrans() @ _4t5.getTrans()
                            testVec = np.matmul(_0t4, np.array([1, 1, 1, 1]))
                            #print(testVec[:3])
                            points.append(testVec[:3])
                            p.update(t, advance=1)
    if _save == True:
        with open(_file + ".csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["x", "y", "z"])   # Kopfzeile
            writer.writerows(points)
            
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=200, origin=[0, 0, 0])
    o3d.visualization.draw_geometries([pcd, axes])
