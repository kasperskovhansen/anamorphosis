from geom_3d.geom_3d import *

class Data_anamorphosis:
    def __init__(self):
        self.objects = []
        self.selectedId = None
        self.selectedIdx = 0

    def addObject(self, obj):
        self.objects.append(obj)

    def setSelectedId(self, selectedId):
        self.selectedId = selectedId
        self.selectedIdx = self.getSelectedIdx()

    def getSelectedIdx(self):
        for i in range(len(self.objects)):
            if str(self.objects[i].id) == str(self.selectedId):
                return i

    def getObjects(self):
        return self.objects

    def getObjType(self, objType: str):
        objects = []
        for obj in self.objects:
            if obj.objType == objType:
                objects.append(obj)
        return objects