from geom_3d.geom_3d import *

class Data_anamorphosis:
    def __init__(self, viewPoint: Point, plane: list):
        self.objects = []
        self.viewPoint = viewPoint
        self.planeP = plane
        # Matematisk repræsentation af planen.
        self.plane = Plane.createFromThreePoints(self.planeP[0], self.planeP[1], self.planeP[2])

    def addObject(self, obj):
        self.objects.append(obj)

    def getObjects(self):
        return self.objects
