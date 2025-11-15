import numpy as np
import open3d as o3d
from visualicationFuctions import *
def main(_file):
    global pcd, polline_set, origin, vis, mat #for toggeling Visu
    # === 1. CSV einlesen ===
    # Ersetze den Dateinamen, falls nötig
    datei = _file

    # CSV einlesen, Kopfzeile überspringen
    punkte = np.loadtxt(datei, delimiter=",", skiprows=1)

    print(f"✅ {punkte.shape[0]} Punkte geladen aus '{datei}'")
    x_max, y_max, z_max = np.max(punkte, axis=0)
    print(f"Max values → X: {x_max}, Y: {y_max}, Z: {z_max}")

    # --- Initialize GUI / Application ---
    app = o3d.visualization.gui.Application.instance
    app.initialize()
    vis = o3d.visualization.O3DVisualizer("Transparent Point Cloud", 1280, 800)

    lines, text = drawScale(x_max, y_max, z_max)
    vis.add_geometry("sclae Lines", lines)

    count = 0
    for i in text:
        count +=1
        vis.add_geometry(f"scale_text_{count}", i)
    #vis.add_geometry("text", i)
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
    vis.add_geometry("Hull", polline_set)
    ##########################################################################################

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(punkte)
    mat = o3d.visualization.rendering.MaterialRecord()
    mat.shader = "defaultUnlit"
    mat.point_size = 1.5
    mat.base_color = [0.0, 0.0, 1.0, 0.3]  # RGBA → 30% opacity
    vis.add_geometry("pcd", pcd, mat)

    origin = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=[0, 0, 0])
    vis.add_geometry("origin", origin)
    vis.add_geometry("SolarPanel", solar_Panel())
    app.run()