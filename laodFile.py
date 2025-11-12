import numpy as np
import open3d as o3d
from visualicationFuctions import *


state = {"pcd_visible": True, "poly_visible": True, "Origin_visible": True}

def toggle_pcd(vis ):
    if state["pcd_visible"]:
        vis.remove_geometry(pcd, reset_bounding_box=False)
    else:
        vis.add_geometry(pcd, reset_bounding_box=False)
    state["pcd_visible"] = not state["pcd_visible"]
    return False

def toggle_poly(vis):
    if state["poly_visible"]:
        vis.remove_geometry(polline_set, reset_bounding_box=False)
    else:
        vis.add_geometry(polline_set, reset_bounding_box=False)
    state["poly_visible"] = not state["poly_visible"]
    return False

def toggle_Origin(vis):
    if state["poly_visible"]:
        vis.remove_geometry(origin, reset_bounding_box=False)
    else:
        vis.add_geometry(origin, reset_bounding_box=False)
    state["poly_visible"] = not state["poly_visible"]
    return False

def view_top_down(vis):
    """Switch camera to look down the Z-axis (XY plane view)."""
    ctr = vis.get_view_control()
    ctr.set_front([0, 0, -1])   # Camera looks downward along -Z
    ctr.set_up([0, 1, 0])       # Y is up
    ctr.set_lookat([0, 0, 0])   # Center point
    vis.update_renderer()
    return False

def main(_file):
    global pcd, polline_set, origin #for toggeling Visu
    # === 1. CSV einlesen ===
    # Ersetze den Dateinamen, falls nötig
    datei = _file

    # CSV einlesen, Kopfzeile überspringen
    punkte = np.loadtxt(datei, delimiter=",", skiprows=1)

    print(f"✅ {punkte.shape[0]} Punkte geladen aus '{datei}'")
    x_max, y_max, z_max = np.max(punkte, axis=0)
    print(f"Max values → X: {x_max}, Y: {y_max}, Z: {z_max}")

    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()
    lines, text = drawScale(x_max, y_max, z_max)
    vis.add_geometry(lines)

    for i in text:
        vis.add_geometry(i)

    ### Hull only 2D####################################################################
    firstZ = punkte[0][2]
    twoD_data = []
    print(firstZ)
    for i in punkte:
        #print(i)
        if i[2] != firstZ:
            break
        twoD_data.append(i[:2])
    #print(twoD_data)
    polline_set = create2DHull(twoD_data, 0.1) #alpha = 0.05 for Hull generation bigger Number trys to get near every Point
    vis.add_geometry(polline_set)
    ##########################################################################################

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(punkte)
    origin = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=[0, 0, 0])
    vis.add_geometry(origin)
    vis.add_geometry(pcd)
    vis.add_geometry(solar_Panel())

    vis.register_key_callback(ord("P"), toggle_pcd)
    vis.register_key_callback(ord("H"), toggle_poly)
    vis.register_key_callback(ord("O"), toggle_Origin)
    vis.register_key_callback(ord("T"), view_top_down)

    print("P: Toggle Points visibilty")
    print("H: Toggle Hull visibilty")
    print("O: Toggle Origin visibilty")
    print("T: Top Down on XY")
    print("If the Hull is looking bad change alpha on line 70 in loadFile.py")

    vis.run()