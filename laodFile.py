import numpy as np
import open3d as o3d
import classesDH
import alphashape

# === 1. CSV einlesen ===
# Ersetze den Dateinamen, falls nötig
datei = "newTest.csv"

# CSV einlesen, Kopfzeile überspringen
punkte = np.loadtxt(datei, delimiter=",", skiprows=1)

print(f"✅ {punkte.shape[0]} Punkte geladen aus '{datei}'")
x_max, y_max, z_max = np.max(punkte, axis=0)
print(f"Max values → X: {x_max}, Y: {y_max}, Z: {z_max}")

lines, text = classesDH.drawScale(x_max, y_max, z_max)

### Hull only 2D####################################################################
firstZ = punkte[0][2]
twoD_data = []
print(firstZ)
for i in punkte:
    #print(i)
    if i[2] != firstZ:
        break
    twoD_data.append(i[:2])

x_min, y_min = np.min(twoD_data, axis=0)
shape = alphashape.alphashape(twoD_data, 0.05)

polygon_points = np.array(shape.exterior.coords)
polygon_points_3d = np.hstack([polygon_points, np.zeros((polygon_points.shape[0], 1))])  # z=0
# Create lines for the edges of the polygon
plines = [[i, i+1] for i in range(len(polygon_points_3d)-1)]
plines.append([len(polygon_points_3d)-1, 0])  # close the polygon

polline_set = o3d.geometry.LineSet(
    points=o3d.utility.Vector3dVector(polygon_points_3d),
    lines=o3d.utility.Vector2iVector(plines)
)
polline_set.colors = o3d.utility.Vector3dVector([[1, 0, 0] for _ in plines])  # red color
polline_set.
##########################################################################################

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(punkte)
axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=[0, 0, 0])

o3d.visualization.draw_geometries([pcd, axes, lines, *text, polline_set])
