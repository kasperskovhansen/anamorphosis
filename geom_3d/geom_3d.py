import math

class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def coords(self):
        return [self.x, self.y, self.z]

    def __str__(self):
        '''
        Her defineres hvordan et punkt skal printes til konsollen
        '''
        return "({}, {}, {})".format(self.x, self.y, self.z)

class Vector(Point):
    def __init__(self, x, y, z):
        Point.__init__(self, x, y, z)

    @classmethod
    def connect(cls, p1, p2):
        '''
        Returnerer en forbindende vektor mellem to punkter
        '''
        return cls(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)

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

    def __str__(self):
        '''
        Her defineres hvordan en vektor skal printes til konsollen
        '''
        return "<{}, {}, {}>".format(self.x, self.y, self.z)


class Line():
    def __init__(self, p0, d):
        self.p0 = p0
        self.d = d

    @classmethod
    def createNew(cls, x0, y0, z0, a, b, c):
        '''
        Lav en ny linje ud fra et punkt og en retningsvektor
        '''
        p0 = Point(x0, y0, z0)
        d = Vector(a,b,c)
        return cls(p0, d)

    @classmethod
    def createTwoPoints(cls, p1, p2):
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

    def getXPoint(self, x):
        '''
        Returnerer et punkt på linjen, svarende til en given x-værdi
        '''
        if self.d.x == 0: return self.point(0)
        #Find den tilsvarende t-værdi
        t = (x-self.p0.x)/self.d.x
        return self.point(t)

    def getYPoint(self, y):
        '''
        Returnerer et punkt på linjen, svarende til en given y-værdi
        '''
        if self.d.y == 0: return self.point(0)
        t = (y - self.p0.y) / self.d.y
        return self.point(t)

    def getZPoint(self, z):
        '''
        Returnerer et punkt på linjen, svarende til en given z-værdi
        '''
        if self.d.z == 0: return self.point(0)
        t = (z - self.p0.z) / self.d.z
        return self.point(t)

    def __str__(self):
        '''
        Her defineres hvordan linjen skal printes til konsollen
        '''
        return "(x,y,z) = <{}, {}, {}> + t*<{}, {}, {}>".format(self.p0.x, self.p0.y, self.p0.z, self.d.x, self.d.y, self.d.z)


class Plane():
    def __init__(self, p0, d1, d2):
        self.p0 = p0
        self.d1 = d1
        self.d2 = d2
    
    @classmethod
    def createFromThreePoints(cls, p1, p2, p3):
        d1 = Vector.connect(p1, p2)
        d2 = Vector.connect(p1, p3)
        return cls(p1, d1, d2)

    @classmethod
    def createFromPointNormal(cls, p1, n):
        pass


def intersection(pl, l):
    #Skæringspunkt mellem plan og linje
    plZ = pl.p0.z
    return l.getZPoint(plZ)

def distancePointPlane(p0, pl):
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

def dot(v1: Vector, v2: Vector) -> float:
    '''
    Returner prikproduktet mellem v1 og v2
    '''
    #prøv selv
    return v1.x * v2.x + v1.y * v2.y

def cross(v1: Vector, v2: Vector) -> Vector:
    x = v1.y * v2.z - v1.z * v2.y
    y = v1.x * v2.z - v1.z * v2.x
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

def distance(p1, p2):
    # Afstand mellem to punkter
    return Vector.connect(p1, p2).length()

def distancePointLine(P, l):
    return cross(l.d, Vector.connect(l.p0, P)).length() / l.d.length()

if __name__ == "__main__":
    #Her testes biblioteket, hvis det køres som main-program.
    #Hvis biblioteket i stedet importeres til et andet program, springes nedenstående kode over

    p1 = Point(0,0,1)
    p2 = Point(1,1,0)
    print(p1, p2)

    v1 = Vector.fromPoint(p1)
    v2 = Vector(p2.x, p2.y, p2.z)
    print(v1, v2)

    l1 = Line.createTwoPoints(p1,p2)
    print(l1)
    p3 = l1.getXPoint(1)
    print(p3)
    print(v1.length())
    
    v3 = Vector(2,0,0)
    v4 = Vector(1,2,1)
    print([v3, v4, perpendicular(v3,v4)])

    p6 = Point(0,0,0)
    l7 = Line(Point(4,0,0), Vector(0,1,0))
    print("Dist: " + str(distancePointLine(p6, l7)))