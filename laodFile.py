import numpy as np
import open3d as o3d
import classesDH

# === 1. CSV einlesen ===
# Ersetze den Dateinamen, falls nötig
datei = "test.csv"

# CSV einlesen, Kopfzeile überspringen
punkte = np.loadtxt(datei, delimiter=",", skiprows=1)

print(f"✅ {punkte.shape[0]} Punkte geladen aus '{datei}'")
x_max, y_max, z_max = np.max(punkte, axis=0)
print(f"Max values → X: {x_max}, Y: {y_max}, Z: {z_max}")

lines, text = classesDH.drawScale(x_max, y_max, z_max)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(punkte)
axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=[0, 0, 0])

o3d.visualization.draw_geometries([pcd, axes, lines, *text])
