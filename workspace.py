import numpy as np
import open3d as o3d
import classesDH as dh
      
_0t1 = dh.Cdh_trans(90, -90, 200, 0, 20, 20000, 0)
_1t2 = dh.Cdh_rot(0, 2000, 0, 0, 5, 360, 0)
_2t3 = dh.Cdh_rot(0, 1000, 0, 0, 5, 360, 0)
_3t4 = dh.Cdh_rot(0, 500, 0, 0, 5, 360, 0)

step1=0
step2=0

points = []
while step1 < (20000/_0t1.getStepSize()): #500mm in trans
    #print("step1: " + str(step1))
    step1 += _0t1.getStepSize()
    _0t1.makeStep()
    #step2 = 0
    #while step2 < (360/5):
        #print("step2: " + str(step2))
    #step2 += 5
    #_1t2.makeStep()
    #_0t4 = _0t1.getTrans() * _1t2.getTrans() #* _2t3.getTrans() * _3t4.getTrans()
    _0t4 = _0t1.getTrans() @ _1t2.getTrans()
    print("New Trans: ")
    print(_0t4)
    testVec = np.matmul(_0t4, np.array([1, 1, 1, 1]))
    print(testVec[:3])
    points.append(testVec[:3])

#print(points)
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.3, origin=[0, 0, 0])
o3d.visualization.draw_geometries([pcd])
