import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from geom_3d.geom_3d import *

# Animation
# https://www.youtube.com/watch?v=ZmYPzESC5YY
import matplotlib.animation as animation

from datetime import datetime
initialTime = datetime.now()


# Opsætning
fig = plt.figure()
ax = Axes3D(fig)
ax.azim = 40
ax.elev = 1

figPoints = []

shouldAnimate = False
animationInterval = 1000

def pointsToCoords(l: list) -> list:
    # Transponer listen med koordinatsæt, så vi får tre lister med henholdsvis x, y, og z.
    coordsList = []
    for p in l:
        coordsList.append(p.coords())
    return np.transpose(coordsList)

def linesToCoords(lines: list) -> list:
    coordsList = []
    for l in lines:
        coordsList.append([[l.p0.x, l.d.x + l.p0.x], [l.p0.y, l.d.y + l.p0.y], [l.p0.z, l.d.z + l.p0.z]])
    return coordsList


def getLines(figPoints: list, viewPoint: Point):
    lineList = []
    for point in figPoints:
        lineList.append(Line.createTwoPoints(point, viewPoint))
    return lineList


def animate(i):
    ax.clear()
    # Plan der agerer gulv
    pPoints = [Point(0,0,0), Point(10,0,0), Point(10,10,0), Point(0,10,0)]
    T = pointsToCoords(pPoints)
    verts = [list(zip(T[0],T[1],T[2]))]
    # Tilføj plan til tegningen.
    ax.add_collection3d(Poly3DCollection(verts, alpha=0.5))

    # Matematisk repræsentation af planen.
    plane = Plane(pPoints[0], pPoints[1], pPoints[2])


    # Punkt hvorfra iagttageren observerer.
    viewPoint = Point(0.5,0,8)
    ax.scatter(viewPoint.x, viewPoint.y, viewPoint.z, color='green')


    # Punkter i 3D figuren, der senere skal vises som anamorfose.
    # Box pos
    bpX = 4 + 0.1 * i
    bpY = 4
    bpZ = 0.5
    # Box width
    bW = 2
    figPoints = [Point(bpX, bpY, bpZ), Point(bpX + bW, bpY, bpZ), Point(bpX + bW, bpY + bW, bpZ), Point(bpX, bpY + bW, bpZ), Point(bpX, bpY, bpZ + bW), Point(bpX + bW, bpY, bpZ + bW), Point(bpX + bW, bpY + bW, bpZ + bW), Point(bpX, bpY + bW, bpZ + bW)]

    T = pointsToCoords(figPoints)
    # Tilføj alle punkterne til tegningen.
    ax.scatter(T[0], T[1], T[2], color='red')


    # Linjer mellem viewPoint og figPoints.
    lines = getLines(figPoints, Vector.fromPoint(viewPoint))
    coordsList = linesToCoords(lines)

    for line in coordsList:
        ax.plot(line[0], line[1], line[2], color='blue', linestyle=':')

    # Lister over punkter projiceret på planen.
    pointsOnPlane = []
    for line in lines:
        pointsOnPlane.append(intersection(plane, line))

    T = pointsToCoords(pointsOnPlane)
    ax.scatter(T[0], T[1], T[2], color='blue')


if shouldAnimate:  
    ani = animation.FuncAnimation(fig, animate, interval=animationInterval)
else:
    animate(0)


endTime = datetime.now()
print("Deltatime: " + str(endTime - initialTime))
plt.show()
