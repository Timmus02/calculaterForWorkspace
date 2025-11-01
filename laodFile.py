import numpy as np
import open3d as o3d

# === 1. CSV einlesen ===
# Ersetze den Dateinamen, falls nötig
datei = "test.csv"

# CSV einlesen, Kopfzeile überspringen
punkte = np.loadtxt(datei, delimiter=",", skiprows=1)

print(f"✅ {punkte.shape[0]} Punkte geladen aus '{datei}'")

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(punkte)
axes = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=[0, 0, 0])

o3d.visualization.draw_geometries([pcd, axes])
