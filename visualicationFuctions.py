import open3d as o3d
import trimesh
from shapely.geometry import Polygon, MultiPolygon
from shapely.geometry import MultiPoint
from shapely.ops import unary_union
from matplotlib.textpath import TextPath
import numpy as np
import alphashape

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
    _Xmax = step # the scale line goes to the end and not only to max point
    step = 0
    while step < _Ymax:
        step += 50
        ScalePoints = np.append(ScalePoints,  [[20, step, 0]], axis=0) #axis = 0 ansosnten wird das array geflatted
        ScalePoints = np.append(ScalePoints, [[-20, step, 0]], axis=0)
        ScaleLines = np.append(ScaleLines, [[len(ScalePoints)-2, len(ScalePoints)-1]], axis=0)
    _Ymax = step
    step = 0
    while step < _Zmax:
        step += 50
        ScalePoints = np.append(ScalePoints,  [[0, 20, step]], axis=0) #axis = 0 ansosnten wird das array geflatted
        ScalePoints = np.append(ScalePoints, [[0, -20, step]], axis=0)
        ScaleLines = np.append(ScaleLines, [[len(ScalePoints)-2, len(ScalePoints)-1]], axis=0)
    _Zmax = step

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

def create2DHull(points, alpha):
    shape = alphashape.alphashape(points, alpha)
    print(type(shape))
    if isinstance(shape, MultiPolygon):
        shape = unary_union(shape)
        print(type(shape))
        # If still MultiPolygon, make alternative convex hull
        if isinstance(shape, MultiPolygon):
            print("Alphashade not working!!! --> using convex Hull")
            shape = MultiPoint(points).convex_hull
    if shape.is_empty:
        return None   
    
    polygon_points = np.array(shape.exterior.coords)
    polygon_points_3d = np.hstack([polygon_points, np.zeros((polygon_points.shape[0], 1))])  # z=0
    # Create lines for the edges of the polygon
    plines = [[i, i+1] for i in range(len(polygon_points_3d)-1)]
    plines.append([len(polygon_points_3d)-1, 0])  # close the polygon

    polline_set = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(polygon_points_3d),
        lines=o3d.utility.Vector2iVector(plines)
    )
    polline_set.colors = o3d.utility.Vector3dVector([[0, 0, 0] for _ in plines])  # red color
    return polline_set