import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
datei = "newTest.csv"

# CSV einlesen, Kopfzeile überspringen
punkte = np.loadtxt(datei, delimiter=",", skiprows=1)

print(f"✅ {punkte.shape[0]} Punkte geladen aus '{datei}'")
x_max, y_max, z_max = np.max(punkte, axis=0)
print(f"Max values → X: {x_max}, Y: {y_max}, Z: {z_max}")

firstZ = punkte[0][2]
twoD_data = []
print(firstZ)
for i in punkte:
    #print(i)
    if i[2] != firstZ:
        break
    twoD_data.append(i[:2])

hull = ConvexHull(twoD_data)
plt.plot(punkte[:, 0], punkte[:, 1], 'o', label='Points')

# Plot hull edges
for simplex in hull.simplices:
    plt.plot(punkte[simplex, 0], punkte[simplex, 1], 'r-')

# Optionally close the hull loop
plt.plot(punkte[hull.vertices, 0], punkte[hull.vertices, 1], 'r--', lw=2, label='Convex Hull')
plt.plot(punkte[hull.vertices[0], 0], punkte[hull.vertices[0], 1], 'ro')

plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('2D Convex Hull')
plt.axis('equal')
plt.show()