import math
import uuid
import numpy as np

class Point():
    def __init__(self, x: (float,int), y: (float,int), z: (float,int)):
        self.x = x
        self.y = y
        self.z = z

    def coords(self):
        return [self.x, self.y, self.z]

    def translate(self, d):
        self.x += d.x
        self.y += d.y
        self.z += d.z

    def add(self, p1):
        self.x += p1.x
        self.y += p1.y
        self.z += p1.z

    def __str__(self):
        '''
        Her defineres hvordan et punkt skal printes til konsollen
        '''
        return "({}, {}, {})".format(self.x, self.y, self.z)

class Vector(Point):
    def __init__(self, x: (float,int), y: (float,int), z: (float,int)):
        Point.__init__(self, x, y, z)

    @classmethod
    def connect(cls, p1: Point, p2: Point):
        '''
        Returnerer en forbindende vektor mellem to punkter
        '''
        return cls(p2.x - (p1.x), p2.y - (p1.y), p2.z - (p1.z))

    @classmethod
    def fromPoint(cls, p: Point):
        '''
        Lav en ny stedvektor ud fra et punkt
        '''
        return cls(p.x, p.y, p.z)

    def length(self) -> float:
        '''
        Denne funktion skal udregne længden af vektoren, og returnere tallet
        '''
        #Prøv selv
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def add(self, v1) -> None:        
        self.x += v1.x
        self.y += v1.y
        self.z += v1.z        


    def subtract(self, v1) -> None:        
        self.x -= v1.x
        self.y -= v1.y
        self.z -= v1.z

    def __str__(self):
        '''
        Her defineres hvordan en vektor skal printes til konsollen
        '''
        return "<{}, {}, {}>".format(self.x, self.y, self.z)


class Line():
    def __init__(self, p0: Point, d: Vector):
        self.p0 = p0
        self.d = d

    @classmethod
    def createNew(cls, x0: (float, int), y0: (float, int), z0: (float, int), a: (float, int), b: (float, int), c: (float, int)):
        '''
        Lav en ny linje ud fra et punkt og en retningsvektor
        '''
        p0 = Point(x0, y0, z0)
        d = Vector(a,b,c)
        return cls(p0, d)

    @classmethod
    def createTwoPoints(cls, p1: Point, p2: Point):
        '''
        Lav en ny linje ud fra to punkter på linjen
        '''
        d = Vector.connect(p1, p2)
        p0 = Vector(p1.x, p1.y, p1.z) # Skulle det ikke have været: p0 = p1
        return cls(p0, d)

    def point(self, t: (float,int) = 0) -> Point:
        '''
        Returnerer et punkt på linjen, svarende til en given t-værdi
        '''
        if not isinstance(t, (float, int)):
            raise TypeError('t har ikke en gyldig værdi')

        p = Vector.fromPoint(self.p0)
        s = scale(t, self.d)
        return add(p,s)

    def getXPoint(self, x: (float, int)):
        '''
        Returnerer et punkt på linjen, svarende til en given x-værdi
        '''
        if self.d.x == 0: return self.point(0)
        #Find den tilsvarende t-værdi
        t = (x-self.p0.x)/self.d.x
        return self.point(t)

    def getYPoint(self, y: (float, int)):
        '''
        Returnerer et punkt på linjen, svarende til en given y-værdi
        '''
        if self.d.y == 0: return self.point(0)
        t = (y - self.p0.y) / self.d.y
        return self.point(t)

    def getZPoint(self, z: (float, int)):
        '''
        Returnerer et punkt på linjen, svarende til en given z-værdi
        '''
        if self.d.z == 0: return self.point(0)
        t = (z - self.p0.z) / self.d.z
        return self.point(t)

    def getPointT(self, p: Point):
        print(self)
        print(p)
        t = (p.x - self.p0.x) / self.d.x
        print(t)
        print("t * self.d.y + self.p0.y == p.y  ->  {} == {}".format(t * self.d.y + self.p0.y,p.y))
        if plusMinus(t * self.d.y + self.p0.y, p.y):
            print(t)
            return t
        return None


    def __str__(self):
        '''
        Her defineres hvordan linjen skal printes til konsollen
        '''
        return "(x,y,z) = <{}, {}, {}> + t*<{}, {}, {}>".format(self.p0.x, self.p0.y, self.p0.z, self.d.x, self.d.y, self.d.z)


class Segment():
    def __init__(self, v1: Vector, v2: Vector):
        self.v1 = v1
        self.v2 = v2

    def __str__(self):
        return "({}, {}, {}), ({}, {}, {})".format(self.v1.x, self.v1.y, self.v1.z, self.v2.x, self.v2.y, self.v2.z)

class Plane():
    def __init__(self, p0: Point, d1: Vector, d2: Vector):
        self.p0 = p0
        self.d1 = d1
        self.d2 = d2
    
    @classmethod
    def createFromThreePoints(cls, p1: Point, p2: Point, p3: Point):
        d1 = Vector.connect(p1, p2)
        d2 = Vector.connect(p1, p3)
        return cls(p3, d1, d2)

    @classmethod
    def createFromPointNormal(cls, p1: Point, n: Vector):
        pass


class Object():
    def __init__(self, points: [Point], segments: [Segment] = None, objType: str = "", name: str = "", scale: (float, int) = 1, deleteable: bool = True, mathPlane: Plane = None, startVec: Vector = Vector(0,0,0)):
        self.points = points
        self.segments = segments
        self.objType = objType
        self.name = name
        self.id = uuid.uuid4() 
        
        self.startVec = startVec
        self.xAng = 0
        self.yAng = 0
        self.zAng = 0
        self.centerPoint = self.calcCenterPoint()
        
        self.scale=scale
        self.deleteable = deleteable        
        self.mathPlane = mathPlane        
    @classmethod
    def createType(cls, objType: str, scale: float, v0: Vector, name: str = "", deleteable: bool = True):
        if objType == "Kasse":
            # Box pos
            bpX = v0.x
            bpY = v0.y
            bpZ = v0.z
            # Box width
            bW = scale
            # Figur punkter.
            # fp = [Vector(bpX, bpY, bpZ), Vector(bpX + bW, bpY, bpZ), Vector(bpX + bW, bpY + bW, bpZ), Vector(bpX, bpY + bW, bpZ), Vector(bpX, bpY, bpZ + bW), Vector(bpX + bW, bpY, bpZ + bW), Vector(bpX + bW, bpY + bW, bpZ + bW), Vector(bpX, bpY + bW, bpZ + bW)]
            # segments = [Segment(fp[0],fp[1]), Segment(fp[0],fp[3]), Segment(fp[0],fp[4]), Segment(fp[1],fp[2]), Segment(fp[1],fp[5]), Segment(fp[2],fp[3]), Segment(fp[2],fp[6]), Segment(fp[3],fp[7]), Segment(fp[4],fp[5]), Segment(fp[5],fp[6]), Segment(fp[6],fp[7]), Segment(fp[4],fp[7])]
            fp = [Vector(bpX + bW, bpY, bpZ + bW), Vector(bpX + bW, bpY + bW, bpZ + bW)]
            segments = [Segment(fp[0], fp[1])]
            return cls(fp, segments=segments, objType=objType, name = name, scale=scale, startVec=v0)

        elif objType == "Observationspunkt":
            return cls([Vector(v0.x,v0.y,v0.z)], deleteable=deleteable, objType=objType, name = name, scale=scale, startVec=v0)
        
        elif objType == "Plan":
            # Figur punkter.
            fp = [Vector(v0.x, v0.y, v0.z), Vector(v0.x + scale, v0.y, v0.z), Vector(v0.x + scale, v0.y + scale, v0.z), Vector(v0.x, v0.y + scale, v0.z)]
            segments = [Segment(fp[0], fp[1]), Segment(fp[1], fp[2]), Segment(fp[2], fp[3]), Segment(fp[0], fp[3])]
            # Matematisk repræsentation af planen.
            mathPlane = Plane.createFromThreePoints(fp[0], fp[1], fp[2])
            return cls(fp, segments=segments, deleteable=deleteable, objType=objType, name = name, scale=scale, mathPlane=mathPlane, startVec=v0)
        
        elif objType == "Icosahedron":
            h = 0.5*(1+np.sqrt(5))
            p1 = np.array([[0, 1, h], [0, 1, -h], [0, -1, h], [0, -1, -h]])
            p2 = p1[:, [1, 2, 0]]
            p3 = p1[:, [2, 0, 1]]
            arr = np.vstack((p1, p2, p3))
            
            fp = []
            for point in arr:                
                fp.append(Point(point[0], point[1], point[2]))
            return cls(fp, objType=objType, name = name, scale=scale, startVec=v0)

        elif objType == "Tetrahedron":
            pass
    
    def calcCenterPoint(self):
        if len(self.points) == 1:
            return self.points[0]
        
        xList, yList, zList = [], [], []        
        for point in self.points:
            coords = point.coords()
            xList.append(coords[0])
            yList.append(coords[1])
            zList.append(coords[2])
        xList.sort()
        yList.sort()
        zList.sort()
        xCoord = (xList[-1] - xList[0]) / 2
        yCoord = (yList[-1] - yList[0]) / 2
        zCoord = (zList[-1] - zList[0]) / 2
        vec = Vector(xCoord, yCoord, zCoord)
        vec.add(self.startVec)
        return vec


    def applyRotation(self, xAng: (float, int), yAng: (float, int), zAng: (float, int)):
        self.Rx = np.array([[1,0,0], [0,math.cos(xAng), math.sin(xAng)], [0, -math.sin(xAng), math.cos(xAng)]])
        self.Ry = np.array([[math.cos(yAng),0,-math.sin(yAng)], [0, 1, 0], [math.sin(yAng), 0, math.cos(yAng)]])
        self.Rz = np.array([[math.cos(zAng), math.sin(zAng),0], [-math.sin(zAng), math.cos(zAng), 0], [0, 0, 1]])
        
        for point in self.points:
            point.subtract(self.centerPoint)
            vec = np.array([point.x, point.y, point.z])
            vec = self.Rx.dot(vec)
            vec = self.Ry.dot(vec)
            vec = self.Rz.dot(vec)
            point.x = vec[0]
            point.y = vec[1]
            point.z = vec[2]
            point.add(self.centerPoint)

        print(self.objType)
        if self.objType == "Plan":
            print("Plan")
            self.mathPlane = Plane.createFromThreePoints(self.points[0], self.points[1], self.points[2])

    def __str__(self):
        '''
        Her defineres hvordan linjen skal printes til konsollen
        '''
        return "{}".format(self.points)

    def rotate(self, axis: str, degrees: float):
        '''
        Drej figuren om centerPoint og den givne akse med et bestemt antal grader.
        '''
        pass

    def translate(self, d: Vector):
        '''
        Translater figuren med vektoren d.
        '''
        # self.centerPoint.translate(d)
        for point in self.points:
            point.translate(d)
        self.centerPoint.translate(d)    

def lineLineIntersection(l1: Line, l2: Line):
    intersection = lineLineIntersectionCalc(l2, l1)
    print("Intersection: {}".format(intersection))
    if not intersection:
        print("Intersection: {}".format(intersection))
        intersection2 = lineLineIntersectionCalc(l1, l2)
        print("Intersection2: {}".format(intersection2))
        if intersection2:
            return intersection2        
    return intersection
    
def lineLineIntersectionCalc(l1: Line, l2: Line):
    '''
    Skæringspunkt mellem to linjer i rummet.
    '''
    
    # # Line 1
    # Vector(x,y,z) = l1.p0 + s * l1.d

    # x = l1.p0.x + s * l1.d.x
    # y = l1.p0.y + s * l1.d.y
    # z = l1.p0.z + s * l1.d.z

    # # Line 2
    # Vector(x,y,z) = l2.p0 + t * l2.d

    # x = l2.p0.x + t * l2.d.x
    # y = l2.p0.y + t * l2.d.y
    # z = l2.p0.z + t * l2.d.z


    # Sat sammen

    # x:
    # l1.p0.x + s * l1.d.x = l2.p0.x + t * l2.d.x

    # s = (l2.p0.x + t * l2.d.x - l1.p0.x) / l1.d.x

    # Substituer s i ligningen for y:
    # y:
    # l1.p0.y + s * l1.d.y = l2.p0.y + t * l2.d.y

    # Substitueret:
    print("l2.d.y * l1.d.x - l2.d.x * l1.d.y == 0  ->  {} == {}".format(l2.d.y * l1.d.x - l2.d.x * l1.d.y, 0))
    if l2.d.y * l1.d.x - l2.d.x * l1.d.y == 0:
        print("{} == {}".format(l2.d.y * l1.d.x - l2.d.x * l1.d.y, 0))
        return None
    t = (l1.d.x * (l1.p0.y - l2.p0.y) - l1.p0.x * l1.d.y + l2.p0.x * l1.d.y) / (l2.d.y * l1.d.x - l2.d.x * l1.d.y)

    # Indsæt dette i ligningen for x:
    print("l1.d.x == 0  ->  {} == {}".format(l1.d.x, 0))
    if l1.d.x == 0:
        print("{} == {}".format(l1.d.x, 0))
        return None
    s = (l2.p0.x + t * l2.d.x - l1.p0.x) / l1.d.x

    # Tjek om ligningen for z går op, hvis man substituerer de to:
    # z:
    # l1.p0.z + s * l1.d.z = l2.p0.z + t * l2.d.z

    print("l1.p0.z + s * l1.d.z == l2.p0.z + t * l2.d.z  ->  {} == {}".format(l1.p0.z + s * l1.d.z, l2.p0.z + t * l2.d.z))
    if plusMinus(l1.p0.z + s * l1.d.z, l2.p0.z + t * l2.d.z):
        return Point(l1.p0.x + s * l1.d.x, l1.p0.y + s * l1.d.y, l1.p0.z + s * l1.d.z)
    return None
   


    # # To ligninger med to ubekendte.
    # if not l2.d.x*l1.d.y - l2.d.y * l1.d.x <= 0.001 and not l2.d.x*l1.d.y - l2.d.y * l1.d.x >= -0.001:
    #     t = (l2.p0.y * l1.d.x + l1.p0.x*l1.d.y - l1.p0.y + l2.p0.x*l1.d.y) / (l2.d.x*l1.d.y - l2.d.y * l1.d.x)
    # else:
    #     t = 0
    # if not l1.d.x == 0:
    #     s = (l2.p0.x + t * l2.d.x - l1.p0.x) / l1.d.x
    # else: s = 0
    # # z1 = l1.p0.z + s * l1.d.z
    # # z2 = l2.p0.z + t * l2.d.z
    
    # # x1 = l1.p0.x + s * l1.d.x
    # # x2 = l2.p0.x + t * l2.d.x
    # # # print("x1: " + str(x1) + " x2: " + str(x2))
    # # y1 = l1.p0.y + s * l1.d.y
    # # y2 = l2.p0.y + t * l2.d.y
    # # print("y1: " + str(y1) + " y2: " + str(y2))
    # print("l1.p0.x + t * l1.d.x == l2.p0.x + s * l2.d.x  ->  {} == {}".format(l1.p0.x + t * l1.d.x, l2.p0.x + s * l2.d.x))
    # print("l1.p0.y + t * l1.d.y == l2.p0.y + s * l2.d.y  ->  {} == {}".format(l1.p0.y + t * l1.d.y, l2.p0.y + s * l2.d.y))
    # print("l1.p0.z + t * l1.d.z == l2.p0.z + s * l2.d.z  ->  {} == {}".format(l1.p0.z + t * l1.d.z, l2.p0.z + s * l2.d.z))
    # if l1.p0.x + t * l1.d.x == l2.p0.x + s * l2.d.x and l1.p0.y + t * l1.d.y == l2.p0.y + s * l2.d.y and l1.p0.z + t * l1.d.z == l2.p0.z + s * l2.d.z:

    #     return Point(l1.p0.x + s * l1.d.x, l1.p0.y + s * l1.d.y, l1.p0.z + s * l1.d.z)
    # return None
    # # if z1 == z2:
    # #     # print("s: " + str(s) + " t: " + str(t))
    # #     return Point(l1.p0.x + t * l1.d.x, l1.p0.y + t * l1.d.y, l1.p0.z + t * l1.d.z)
    # # else:
    # #     return None

def isWithinSegments(p0: Point, d: Vector, segments: [Segment]):
    l = Line(p0, d)

    crossings = 0
    intersections = []

    segLines = []
    for seg in segments:
        segLine = Line.createTwoPoints(seg.v1, seg.v2)
        segLines.append(segLine)
        intersection = lineLineIntersection(l, segLine)
        print("intersection {}".format(intersection))
        if intersection and l.getPointT(intersection) >= 0: 
            intersections.append(intersection)

            if onLineBetweenPoints(intersection, seg.v1, seg.v2):
                print("T val: {}".format(l.getPointT(intersection)))
                crossings += 1
                intersections.append(intersection)
    # print(crossings)
    # print("%: {}".format(1 % 2))
    within = None
    if crossings % 2 == 1: within = True
    else: within = False
    print("l for point {} -> {}".format(p0, l))
    return [[l], intersections, segLines, within]

def segmentSegmentIntersection(seg1, segments: [Segment]):
    lineSegs = []
    inters = []

    lineSeg1 = Line.createTwoPoints(seg1.v1, seg1.v2)

    lineSegs.append(lineSeg1)
    for seg2 in segments:
        # print("Segments: {}".format(seg2))

        lineSeg2 = Line.createTwoPoints(seg2.v1, seg2.v2)
        # print("Seg2 {} {}".format(seg1, seg2))
        lineSegs.append(lineSeg2)
        intersection = lineLineIntersection(lineSeg2, lineSeg1)
        # if not intersection:
        #     intersection2 = lineLineIntersection(lineSeg1, lineSeg2)
        #     if not intersection2:
        #         continue
        #     intersection = intersection2
        inters.append(intersection)
        print("segseginters {}".format(intersection))
        if intersection and onLineBetweenPoints(intersection, seg1.v1, seg1.v2) and onLineBetweenPoints(intersection, seg2.v1, seg2.v2):
            return [lineSegs, intersection, inters]
    return [lineSegs, None, inters]
    
def onLineBetweenPoints(pMid: Point, pMin: Point, pMax: Point):
    print("distance(pMid, pMin) + distance(pMid, pMax) == distance(pMin, pMax)  ->  {} == {}".format(distance(pMid, pMin) + distance(pMid, pMax), distance(pMin, pMax)))
    if plusMinus(distance(pMid, pMin) + distance(pMid, pMax), distance(pMin, pMax)):
        print("Is between {} == {}".format(distance(pMid, pMin) + distance(pMid, pMax), distance(pMin, pMax)))
    # if distance(pMid, pMin) + distance(pMid, pMax) >= distance(pMin, pMax) - 0.01 and distance(pMid, pMin) + distance(pMid, pMax) <= distance(pMin, pMax) + 0.01:
        return True
    return False

def intersection(pl: Plane, l: Line):
    '''
    Skæringspunkt mellem plan og linje.
    '''
    # Normalvektoren til planen pl.
    planN = cross(pl.d1, pl.d2)

    # Tjek om linjen er parallel med 
    if dot(planN, l.d) == 0:
        # Linjen og planen er parallelle.
        if planN.x * (l.p0.x - pl.p0.x) + planN.y * (l.p0.y - pl.p0.y) + planN.z * (l.p0.z - pl.p0.z) == 0:
            # Linjen ligger i planen.
            return False

    planEqB = planN.x * pl.p0.x + planN.y * pl.p0.y + planN.z * pl.p0.z

    t = -(planN.x * l.p0.x + planN.y * l.p0.y + planN.z * l.p0.z - planEqB) / (planN.x * l.d.x + planN.y * l.d.y + planN.z * l.d.z)
    
    x = l.p0.x + t * l.d.x
    y = l.p0.y + t * l.d.y
    z = l.p0.z + t * l.d.z

    intersection = Point(x, y, z)
    return intersection


def distancePointPlane(p0: Point, pl: Plane):
    # afstand fra punkt til plan
    pass

def scale(s: (float, int), v: Vector) -> Vector:
    '''
    Returnerer vektoren v, skaleret med s
    '''
    return Vector(v.x * s, v.y * s, v.z * s)

def normalize(v: Vector) -> Vector:
    '''
    Returner en kopi v, der er skaleret til længden 1. (Enhedsvektor)
    '''
    if v.length() > 0.000001:
        s = 1/v.length()
        return Vector(v.x * s, v.y * s, v.z * s)
    else:
        #Retningen er ikke defineret for vektorer uden længde.
        return Vector(0,0,0)

def add(v1: Vector, v2: Vector) -> Vector:
    '''
    Læg to vektorer sammen og returner resultatet
    '''
    #Prøv selv
    return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def plusMinus(x, y):
    margin = 0.0000001
    print("plusMinus: {} == {}".format(x,y))
    if x >= y - margin and x <= y + margin:
        return True
    return False

def subtract(v1: Vector, v2: Vector) -> Vector:
    '''
    Læg to vektorer sammen og returner resultatet
    '''
    #Prøv selv
    return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def dot(v1: Vector, v2: Vector) -> float:
    '''
    Returner prikproduktet mellem v1 og v2
    '''
    #prøv selv
    return v1.x * v2.x + v1.y * v2.y

def cross(v1: Vector, v2: Vector) -> Vector:
    x = v1.y * v2.z - v1.z * v2.y
    y = v1.z * v2.x - v1.x * v2.z
    z = v1.x * v2.y - v1.y * v2.x
    return Vector(x, y, z)

def angle(v1: Vector, v2: Vector):
    if v1.length() > 0.000001 and v2.length() > 0.000001:
        return math.acos(dot(v1,v2)/(v1.length() * v2.length()))
    return None

def perpendicular(v1: Vector, v2: Vector) -> bool:
    # ternary operator
    return True if dot(v1, v2) == 0 else False

def projection(v1: Vector, v2: Vector) -> Vector:
    return (dot(v1, v2)/v2.length()**2)*v2

def distance(p1: Point, p2: Point):
    # Afstand mellem to punkter
    return Vector.connect(p1, p2).length()

def distancePointLine(P: Point, l: Line):
    return cross(l.d, Vector.connect(l.p0, P)).length() / l.d.length()

if __name__ == "__main__":
    #Her testes biblioteket, hvis det køres som main-program.
    #Hvis biblioteket i stedet importeres til et andet program, springes nedenstående kode over

    pass