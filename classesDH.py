import numpy as np
import open3d as o3d
import trimesh
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from matplotlib.textpath import TextPath
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

    def __init__(self, _phi,_alpha, _a, _initalLength, _stepSize, _max, _min):
        self.alpha = _alpha
        self.a = _a
        self.d = _initalLength
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

def make_text_mesh(text, font="Arial", font_size=20.0, depth=1.0):
    """
    Create a 3D Open3D mesh from text (robust to MultiPolygon shapes).
    """
    tp = TextPath((0, 0), text, size=font_size, prop={'family': font})

    # Convert each text outline into a shapely Polygon
    polygons = []
    for p in tp.to_polygons():
        poly = Polygon(p)
        if poly.is_valid and poly.area > 0:
            polygons.append(poly)

    if not polygons:
        raise ValueError(f"Text '{text}' produced no valid polygons!")

    shape = unary_union(polygons)

    # --- Handle both Polygon and MultiPolygon cases ---
    meshes = []
    if isinstance(shape, Polygon):
        shape = [shape]  # wrap in list for consistency
    elif isinstance(shape, MultiPolygon):
        shape = list(shape.geoms)

    for poly in shape:
        try:
            m = trimesh.creation.extrude_polygon(poly, height=depth)
            meshes.append(m)
        except Exception as e:
            print(f"⚠️ Skipping subshape in '{text}': {e}")

    # Combine all extruded parts
    if len(meshes) == 0:
        raise ValueError(f"No meshes could be created for '{text}'")

    mesh2d = trimesh.util.concatenate(meshes)

    # Convert to Open3D mesh
    mesh3d = o3d.geometry.TriangleMesh()
    mesh3d.vertices = o3d.utility.Vector3dVector(mesh2d.vertices)
    mesh3d.triangles = o3d.utility.Vector3iVector(mesh2d.faces)
    mesh3d.compute_vertex_normals()

    return mesh3d

def drawScale(_Xmax, _Ymax, _Zmax):
    step = 0
    ScalePoints = np.empty(shape=(0,3))
    ScaleLines = np.empty(shape=(0, 2))
    while step < _Xmax:
        step += 50
        ScalePoints = np.append(ScalePoints,  [[step, 20, 0]], axis=0) #axis = 0 ansosnten wird das array geflatted
        ScalePoints = np.append(ScalePoints, [[step, -20, 0]], axis=0)
        ScaleLines = np.append(ScaleLines, [[len(ScalePoints)-2, len(ScalePoints)-1]], axis=0)
    step = 0
    while step < _Ymax:
        step += 50
        ScalePoints = np.append(ScalePoints,  [[20, step, 0]], axis=0) #axis = 0 ansosnten wird das array geflatted
        ScalePoints = np.append(ScalePoints, [[-20, step, 0]], axis=0)
        ScaleLines = np.append(ScaleLines, [[len(ScalePoints)-2, len(ScalePoints)-1]], axis=0)
    step = 0
    while step < _Zmax:
        step += 50
        ScalePoints = np.append(ScalePoints,  [[0, 20, step]], axis=0) #axis = 0 ansosnten wird das array geflatted
        ScalePoints = np.append(ScalePoints, [[0, -20, step]], axis=0)
        ScaleLines = np.append(ScaleLines, [[len(ScalePoints)-2, len(ScalePoints)-1]], axis=0)

    textAr = []
    step = 0
    length = 0
    while step < len(ScalePoints)-2:
        step +=2
        length += 1
        pos = ScalePoints[step]
        if pos[1] == 50 and pos[2] == 0 and pos[0] in [20, -20]: #neu anfangen jetzt y Achse
            length = 1
        if pos[2] == 50 and pos[0] == 0 and pos[1] in [20, -20]: #neu anfangen jetzt z Achse
            length = 1
        text= str(int(length*50))
        tmesh = make_text_mesh(text)
        tmesh.translate(pos)
        tmesh.paint_uniform_color([1, 0, 0])
        # --- Rotate text if it belongs to Z-axis ---
        # x y z
        if pos[2] > 0 and pos[0] == 0 and pos[1] in [20, -20]:
            # Rotate around Y-axis so text faces along X
            R = tmesh.get_rotation_matrix_from_xyz((0, -np.pi / 2, 0))
            tmesh.rotate(R, center=pos)
        if pos[1] > 0 and pos[2] == 0 and pos[0] in [20, -20]:
            R = tmesh.get_rotation_matrix_from_xyz((0, -np.pi , 0))
            tmesh.rotate(R, center=pos)
        if pos[0] > 0 and pos[2] == 0 and pos[1] in [20, -20]:
            R = tmesh.get_rotation_matrix_from_xyz((0, -np.pi , 0))
            tmesh.rotate(R, center=pos)
        textAr.append(tmesh)

    ScalePoints = np.append(ScalePoints, [[0, 0, 0]], axis=0) #Haupt Scala
    ScalePoints = np.append(ScalePoints, [[_Xmax, 0, 0]], axis=0)
    ScalePoints = np.append(ScalePoints, [[0, _Ymax, 0]], axis=0)
    ScalePoints = np.append(ScalePoints, [[0, 0, _Zmax]], axis=0)

    ScaleLines = np.append(ScaleLines, [[len(ScalePoints)-4, len(ScalePoints)-3]], axis=0)
    ScaleLines = np.append(ScaleLines, [[len(ScalePoints)-4, len(ScalePoints)-2]], axis=0)
    ScaleLines = np.append(ScaleLines, [[len(ScalePoints)-4, len(ScalePoints)-1]], axis=0)

    return o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(ScalePoints),lines=o3d.utility.Vector2iVector(ScaleLines)), textAr