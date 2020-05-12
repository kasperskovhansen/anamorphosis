import math

class Point():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

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
        p0 = Vector(p1.x, p1.y, p1.z)
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
        #Find den tilsvarende t-værdi
        t = (x-self.p0.x)/self.d.x
        return self.point(t)

    def getYPoint(self, y):
        '''
        Returnerer et punkt på linjen, svarende til en given y-værdi
        '''
        #Prøv selv
        pass

    def __str__(self):
        '''
        Her defineres hvordan linjen skal printes til konsollen
        '''
        return "(x,y,z) = <{}, {}, {}> + t*<{}, {}, {}>".format(self.p0.x, self.p0.y, self.p0.z, self.d.x, self.d.y, self.d.z)




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
    pass


def dot(v1: Vector, v2: Vector) -> float:
    '''
    Returner prikproduktet mellem v1 og v2
    '''
    #prøv selv
    pass



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
    