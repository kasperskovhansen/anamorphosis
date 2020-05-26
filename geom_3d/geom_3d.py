import math
import uuid
import numpy as np

class Point():
    def __init__(self, x: (float,int), y: (float,int), z: (float,int), color="black", alpha=1):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.alpha = alpha

    def coords(self) -> list:
        '''
        Returnerer koordinatsættet som en liste
        '''
        return [self.x, self.y, self.z]        

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
    def from_point(cls, p: Point):
        '''
        Lav en ny stedvektor ud fra et punkt
        '''
        return cls(p.x, p.y, p.z)

    def add(self, v1) -> None:
        '''
        Læg en anden vektor til denne
        '''
        self.x += v1.x
        self.y += v1.y
        self.z += v1.z

    def subtract(self, v1) -> None:       
        '''
        Træk en anden vektor fra denne
        ''' 
        self.x -= v1.x
        self.y -= v1.y
        self.z -= v1.z

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
    def __init__(self, p0: Point, d: Vector):
        self.p0 = p0
        self.d = d

    @classmethod
    def create_new(cls, x0: (float, int), y0: (float, int), z0: (float, int), a: (float, int), b: (float, int), c: (float, int)):
        '''
        Lav en ny linje ud fra et punkt og en retningsvektor
        '''
        p0 = Point(x0, y0, z0)
        d = Vector(a,b,c)
        return cls(p0, d)

    @classmethod
    def create_two_points(cls, p1: Point, p2: Point):
        '''
        Lav en ny linje ud fra to punkter på linjen
        '''
        d = Vector.connect(p1, p2)
        p0 = Vector(p1.x, p1.y, p1.z) # Skulle det ikke have været: p0 = p1 ?
        return cls(p0, d)

    def point(self, t: (float,int) = 0) -> Point:
        '''
        Returnerer et punkt på linjen, svarende til en given t-værdi
        '''
        if not isinstance(t, (float, int)):            
            raise TypeError('t har ikke en gyldig værdi')

        p = Vector.from_point(self.p0)
        s = scale(t, self.d)
        return add(p,s)

    def get_x_point(self, x: (float, int)):
        '''
        Returnerer et punkt på linjen, svarende til en given x-værdi
        '''
        if self.d.x == 0: return self.point(0)
        #Find den tilsvarende t-værdi
        t = (x-self.p0.x)/self.d.x
        return self.point(t)

    def get_y_point(self, y: (float, int)):
        '''
        Returnerer et punkt på linjen, svarende til en given y-værdi
        '''
        if self.d.y == 0: return self.point(0)
        t = (y - self.p0.y) / self.d.y
        return self.point(t)

    def get_z_point(self, z: (float, int)):
        '''
        Returnerer et punkt på linjen, svarende til en given z-værdi
        '''
        if self.d.z == 0: return self.point(0)
        t = (z - self.p0.z) / self.d.z
        return self.point(t)

    def get_point_t(self, p: Point):
        '''
        Returnerer en t-værdi til et givent punkt
        '''
        if not self.d.x == 0:
            t = (p.x - self.p0.x) / self.d.x
            if not self.d.y == 0:
                if plus_minus(t * self.d.y + self.p0.y, p.y):
                    return t
            elif not self.d.z == 0:
                if plus_minus(t * self.d.z + self.p0.z, p.z):
                    return t
        if not self.d.y == 0:
            t = (p.y - self.p0.y) / self.d.y
            if not self.d.x == 0:
                if plus_minus(t * self.d.x + self.p0.x, p.x):
                    return t
            elif not self.d.z == 0:
                if plus_minus(t * self.d.z + self.p0.z, p.z):
                    return t
        if not self.d.z == 0:
            t = (p.z - self.p0.z) / self.d.z
            if not self.d.y == 0:
                if plus_minus(t * self.d.y + self.p0.y, p.y):
                    return t
            elif not self.d.x == 0:
                if plus_minus(t * self.d.x + self.p0.x, p.x):
                    return t
        return None        

    def __str__(self):
        '''
        Her defineres hvordan linjen skal printes til konsollen
        '''
        return "(x,y,z) = <{}, {}, {}> + t*<{}, {}, {}>".format(self.p0.x, self.p0.y, self.p0.z, self.d.x, self.d.y, self.d.z)

class Segment():
    def __init__(self, v1: Vector, v2: Vector, color="black", alpha=1):
        self.v1 = v1
        self.v2 = v2
        self.color = color
        self.alpha = alpha

    def __str__(self):
        return "({}, {}, {}), ({}, {}, {})".format(self.v1.x, self.v1.y, self.v1.z, self.v2.x, self.v2.y, self.v2.z)

class Plane():
    def __init__(self, p0: Point, d1: Vector, d2: Vector, color="blue", alpha=0.5):
        self.p0 = p0
        self.d1 = d1
        self.d2 = d2
        self.color = color
        self.alpha = alpha
    
    @classmethod
    def create_from_three_points(cls, p1: Point, p2: Point, p3: Point):
        '''
        Returnerer en plan ud fra tre punkter
        '''
        d1 = Vector.connect(p1, p2)
        d2 = Vector.connect(p1, p3)
        return cls(p3, d1, d2)

class Object():
    def __init__(self, points: [Point], segments: [Segment] = None, obj_type: str = "", name: str = "", scale: (float, int) = 1, deleteable: bool = True, mathPlane: Plane = None, start_vec: Vector = Vector(0,0,0)):
        self.points = points
        self.segments = segments
        self.obj_type = obj_type
        self.name = name
        self.id = uuid.uuid4() 
        
        self.start_vec = start_vec
        self.x_ang = 0
        self.y_ang = 0
        self.z_ang = 0
        self.center_point = self.calc_center_point()
        self.visible = True
        self.anamorphosis_visible = True
                
        self.scale=scale
        self.deleteable = deleteable        
        self.mathPlane = mathPlane        
    @classmethod
    def create_type(cls, obj_type: str, scale: float, v0: Vector, name: str = "", deleteable: bool = True):
        '''
        Returnerer et objekt af en given type
        '''
        if obj_type == "Kasse":            
            fp_segments = build_fp_segments(v0, scale, obj_type)
            return cls(fp_segments[0], segments=fp_segments[1], obj_type=obj_type, name = name, scale=scale, start_vec=v0)

        if obj_type == "K":            
            fp_segments = build_fp_segments(v0, scale, obj_type)
            return cls(fp_segments[0], segments=fp_segments[1], obj_type=obj_type, name = name, scale=scale, start_vec=v0)

        elif obj_type == "Observationspunkt":
            return cls([Vector(v0.x,v0.y,v0.z)], deleteable=deleteable, obj_type=obj_type, name = name, scale=scale, start_vec=v0)
        
        elif obj_type == "Plan":
            # Figur punkter.
            fp_segments = build_fp_segments(v0, scale, obj_type)
            return cls(fp_segments[0], segments=fp_segments[1], deleteable=deleteable, obj_type=obj_type, name = name, scale=scale, mathPlane=fp_segments[2], start_vec=v0)
        
        elif obj_type == "Icosahedron":
            h = 0.5*(1+np.sqrt(5))
            p1 = np.array([[0, 1, h], [0, 1, -h], [0, -1, h], [0, -1, -h]])
            p2 = p1[:, [1, 2, 0]]
            p3 = p1[:, [2, 0, 1]]
            arr = np.vstack((p1, p2, p3))
            
            fp = []
            for point in arr:                
                fp.append(Point(point[0], point[1], point[2]))
            return cls(fp, obj_type=obj_type, name = name, scale=scale, start_vec=v0)

        elif obj_type == "Tetrahedron":
            pass
    
    def calc_center_point(self):
        '''
        Returnerer figurens centrum
        '''
        if len(self.points) == 1:
            return self.points[0]
        
        x_list, y_list, z_list = [], [], []        
        for point in self.points:
            coords = point.coords()
            x_list.append(coords[0])
            y_list.append(coords[1])
            z_list.append(coords[2])
        x_list.sort()
        y_list.sort()
        z_list.sort()
        x_coord = (x_list[-1] - x_list[0]) / 2
        y_coord = (y_list[-1] - y_list[0]) / 2
        z_coord = (z_list[-1] - z_list[0]) / 2
        vec = Vector(x_coord, y_coord, z_coord)
        vec.add(self.start_vec)
        return vec

    def apply_rotation(self, x_ang: (float, int), y_ang: (float, int), z_ang: (float, int)):
        '''
        Multiplicerer alle objektets punkter med en rotationsmatrix og roterer dermed figuren
        '''
        r_x = np.array([[1,0,0], [0,math.cos(x_ang), math.sin(x_ang)], [0, -math.sin(x_ang), math.cos(x_ang)]])
        r_y = np.array([[math.cos(y_ang),0,-math.sin(y_ang)], [0, 1, 0], [math.sin(y_ang), 0, math.cos(y_ang)]])
        r_z = np.array([[math.cos(z_ang), math.sin(z_ang),0], [-math.sin(z_ang), math.cos(z_ang), 0], [0, 0, 1]])
        
        for point in self.points:
            point.subtract(self.center_point)
            vec = np.array([point.x, point.y, point.z])
            vec = r_x.dot(vec)
            vec = r_y.dot(vec)
            vec = r_z.dot(vec)
            point.x = vec[0]
            point.y = vec[1]
            point.z = vec[2]
            point.add(self.center_point)

        if self.obj_type == "Plan":
            print("Plan")
            self.mathPlane = Plane.create_from_three_points(self.points[0], self.points[1], self.points[2])

    def set_scale(self, scale: (float, int)):
        '''
        Ændrer figurens skalering
        '''
        old_center = self.center_point        
        self.scale = scale
        fp_segments = build_fp_segments(self.start_vec, self.scale, self.obj_type)
        self.points = fp_segments[0]
        self.segments = fp_segments[1]
        self.center_point = self.calc_center_point()
        for point in self.points:
            point.add(subtract(old_center, self.center_point))

    def __str__(self):
        '''
        Her defineres hvordan linjen skal printes til konsollen
        '''
        return "{}".format(self.points)


    def translate(self, d: Vector):
        '''
        Translater figuren med vektoren d.
        '''        
        for point in self.points:
            point.add(d)
        self.center_point.add(d)    

def build_fp_segments(v0, scale, obj_type):
    '''
    Returnerer lister med punkter og med segmenter for et objekt af en given type
    '''
    scale = float(scale)
    mathPlane = None

    if obj_type == "Kasse":       
        fp = [Vector(v0.x, v0.y, v0.z), Vector(v0.x + scale, v0.y, v0.z), Vector(v0.x + scale, v0.y + scale, v0.z), Vector(v0.x, v0.y + scale, v0.z), Vector(v0.x, v0.y, v0.z + scale), Vector(v0.x + scale, v0.y, v0.z + scale), Vector(v0.x + scale, v0.y + scale, v0.z + scale), Vector(v0.x, v0.y + scale, v0.z + scale)]
        segments = [Segment(fp[0],fp[1]), Segment(fp[0],fp[3]), Segment(fp[0],fp[4]), Segment(fp[1],fp[2]), Segment(fp[1],fp[5]), Segment(fp[2],fp[3]), Segment(fp[2],fp[6]), Segment(fp[3],fp[7]), Segment(fp[4],fp[5]), Segment(fp[5],fp[6]), Segment(fp[6],fp[7]), Segment(fp[4],fp[7])]
    elif obj_type == "K":
        scale = scale / 6
        fp = [Vector(v0.x, v0.y, v0.z), Vector(v0.x + 4*scale, v0.y, v0.z), Vector(v0.x + 4*scale, v0.y, v0.z + 6*scale), Vector(v0.x + 8 * scale, v0.y, v0.z), Vector(v0.x + 13 * scale, v0.y, v0.z), Vector(v0.x + 8 * scale, v0.y, v0.z + 8*scale), Vector(v0.x + 13 * scale, v0.y, v0.z + 16 * scale), Vector(v0.x + 8 * scale, v0.y, v0.z + 16 * scale), Vector(v0.x + 4*scale, v0.y, v0.z + 10*scale), Vector(v0.x + 4*scale, v0.y, v0.z + 16 * scale), Vector(v0.x, v0.y, v0.z + 16 * scale), Vector(v0.x, v0.y + 4 * scale, v0.z + 16 * scale),     Vector(v0.x, v0.y + 4 * scale, v0.z), Vector(v0.x + 4*scale, v0.y + 4 * scale, v0.z), Vector(v0.x + 4*scale, v0.y + 4 * scale, v0.z + 6*scale), Vector(v0.x + 8 * scale, v0.y + 4 * scale, v0.z), Vector(v0.x + 13 * scale, v0.y + 4 * scale, v0.z), Vector(v0.x + 8 * scale, v0.y + 4 * scale, v0.z + 8*scale), Vector(v0.x + 13 * scale, v0.y + 4 * scale, v0.z + 16 * scale), Vector(v0.x + 8 * scale, v0.y + 4 * scale, v0.z + 16 * scale), Vector(v0.x + 4*scale, v0.y + 4 * scale, v0.z + 10*scale), Vector(v0.x + 4*scale, v0.y + 4 * scale, v0.z + 16 * scale)]
        segments = []
        for i in range(10):
            segments.append(Segment(fp[i], fp[i + 12], color="grey"))       
        segments.append(Segment(fp[10], fp[11], color="grey"))            
        for i in range(len(fp)):                
            if i >= 11 and i < len(fp) -1:
                segments.append(Segment(fp[i], fp[i + 1], color="green"))
            segments.append(Segment(fp[11], fp[21], color="green"))
            if i >= 0 and i < 10:
                segments.append(Segment(fp[i], fp[i + 1], color="red"))            
            segments.append(Segment(fp[10], fp[0], color="red"))
    elif obj_type == "Plan":
        fp = [Vector(v0.x, v0.y, v0.z), Vector(v0.x + scale, v0.y, v0.z), Vector(v0.x + scale, v0.y + scale, v0.z), Vector(v0.x, v0.y + scale, v0.z)]
        segments = [Segment(fp[0], fp[1]), Segment(fp[1], fp[2]), Segment(fp[2], fp[3]), Segment(fp[0], fp[3])]
        # Matematisk repræsentation af planen.
        mathPlane = Plane.create_from_three_points(fp[0], fp[1], fp[2])

    return [fp, segments, mathPlane]

def line_line_intersection(l1: Line, l2: Line):
    '''
    Returnerer skæringen mellem to linjer som et punkt
    '''
    x_null = False
    y_null = False
    z_null = False

    if plus_minus(l1.d.x, 0) and plus_minus(l2.d.x, 0):
        x_null = True

    if plus_minus(l1.d.y, 0) and plus_minus(l2.d.y, 0):
        y_null = True

    if plus_minus(l1.d.z, 0) and plus_minus(l2.d.z, 0):
        z_null = True

    if x_null and not y_null and not z_null:
        # Isoler x
        intersection = line_line_intersection_calc(l2, l1, solve_for="x")
        if not intersection:        
            intersection2 = line_line_intersection_calc(l1, l2, solve_for="x")
            if intersection2:
                return intersection2    
        return intersection

    elif not x_null and y_null and not z_null:
        # Isoler y
        intersection = line_line_intersection_calc(l2, l1, solve_for="y")
        if not intersection:        
            intersection2 = line_line_intersection_calc(l1, l2, solve_for="y")
            if intersection2:
                return intersection2    
        return intersection

    elif not x_null and not y_null and z_null:
        # Isoler z
        intersection = line_line_intersection_calc(l2, l1, solve_for="z")
        if not intersection:        
            intersection2 = line_line_intersection_calc(l1, l2, solve_for="z")
            if intersection2:
                return intersection2           
        return intersection
    
    elif not x_null and not y_null and not z_null:
        intersection = line_line_intersection_calc(l2, l1, solve_for="all")
        if not intersection:        
            intersection2 = line_line_intersection_calc(l1, l2, solve_for="all")
            if intersection2:
                return intersection2    
        return intersection
    else:
        return None
    
def line_line_intersection_calc(l1: Line, l2: Line, solve_for="all"):
    '''
    Finder skæringspunktet mellem to linjer i rummet
    '''
    if solve_for == "z" or solve_for == "all":
        if not plus_minus(l2.d.y * l1.d.x - l2.d.x * l1.d.y, 0) and not plus_minus(l1.d.x, 0):
            t = (l2.p0.x * l1.d.y - l1.p0.x * l1.d.y - l2.p0.y * l1.d.x + l1.p0.y * l1.d.x) / (l2.d.y * l1.d.x - l2.d.x * l1.d.y)
            s = (l2.p0.x + t * l2.d.x - l1.p0.x) / l1.d.x            
            if plus_minus(l1.p0.z + s * l1.d.z, l2.p0.z + t * l2.d.z):
                return Point(l1.p0.x + s * l1.d.x, l1.p0.y + s * l1.d.y, l1.p0.z + s * l1.d.z)

    if solve_for == "x" or solve_for == "all":
        if not plus_minus(l2.d.z * l1.d.y - l2.d.y * l1.d.z, 0) and not plus_minus(l1.d.y, 0):
            t = (l2.p0.y * l1.d.z - l1.p0.y * l1.d.z - l2.p0.z * l1.d.y + l1.p0.z * l1.d.y) / (l2.d.z * l1.d.y - l2.d.y * l1.d.z)
            s = (l2.p0.y + t * l2.d.y - l1.p0.y) / l1.d.y
            if plus_minus(l1.p0.x + s * l1.d.x, l2.p0.x + t * l2.d.x):
                return Point(l1.p0.x + s * l1.d.x, l1.p0.y + s * l1.d.y, l1.p0.z + s * l1.d.z)
    
    if solve_for == "y" or solve_for == "all":        
        if not plus_minus(l2.d.z * l1.d.x - l2.d.x * l1.d.z, 0) and not plus_minus(l1.d.x, 0):
            t = (l2.p0.x * l1.d.z - l1.p0.x * l1.d.z + l1.p0.z * l1.d.x - l2.p0.z * l1.d.x) / (l2.d.z * l1.d.x - l2.d.x * l1.d.z)
            s = (l2.p0.x + t * l2.d.x - l1.p0.x) / l1.d.x

            if plus_minus(l1.p0.y + s * l1.d.y, l2.p0.y + t * l2.d.y):
                return Point(l1.p0.x + s * l1.d.x, l1.p0.y + s * l1.d.y, l1.p0.z + s * l1.d.z)

    return None


def is_within_segments(p0: Point, d: Vector, segments: [Segment]) -> bool:
    '''
    Finder ud af om et punkt er placeret inden for et polygon
    '''
    l = Line(p0, d)
   
    crossings = 0

    for seg in segments:
        segLine = Line.create_two_points(seg.v1, seg.v2)
        intersection = line_line_intersection(l, segLine)
        if intersection and l.get_point_t(intersection) and l.get_point_t(intersection) >= 0 and on_line_between_points(intersection, seg.v1, seg.v2): 
            crossings += 1
    
    within = None
    if crossings % 2 == 1: within = True
    else: within = False
    return within

def segment_segments_intersection(seg_1, segments: [Segment]):
    '''
    Finder en eventuel skæring mellem to segmenter
    '''
    line_segs = []
    inters = []
    line_seg_1 = Line.create_two_points(seg_1.v1, seg_1.v2)
    line_segs.append(line_seg_1)
    for seg_2 in segments:
        lineseg_2 = Line.create_two_points(seg_2.v1, seg_2.v2)
        line_segs.append(lineseg_2)
        intersection = line_line_intersection(lineseg_2, line_seg_1)        
        inters.append(intersection)
        if intersection and on_line_between_points(intersection, seg_1.v1, seg_1.v2) and on_line_between_points(intersection, seg_2.v1, seg_2.v2):
            return [line_segs, intersection, inters]
    return [line_segs, None, inters]
    
def on_line_between_points(p_mid: Point, p_min: Point, p_max: Point):
    '''
    Finder ud af om et punkt ligger på linjen mellem to punkter
    '''
    if plus_minus(distance(p_mid, p_min) + distance(p_mid, p_max), distance(p_min, p_max)):    
        return True
    return False

def plane_line_intersection(pl: Plane, l: Line):
    '''
    Skæringspunkt mellem plan og linje
    '''
    # Normalvektoren til planen pl.
    plan_n = cross(pl.d1, pl.d2)

    # Tjek om linjen er parallel med planen.
    if dot(plan_n, l.d) == 0:
        # Linjen og planen er parallelle.
        if plan_n.x * (l.p0.x - pl.p0.x) + plan_n.y * (l.p0.y - pl.p0.y) + plan_n.z * (l.p0.z - pl.p0.z) == 0:
            # Linjen ligger i planen.
            return False

    plan_eq_b = plan_n.x * pl.p0.x + plan_n.y * pl.p0.y + plan_n.z * pl.p0.z
    if (plan_n.x * l.d.x + plan_n.y * l.d.y + plan_n.z * l.d.z) == 0:
        return False
    t = -(plan_n.x * l.p0.x + plan_n.y * l.p0.y + plan_n.z * l.p0.z - plan_eq_b) / (plan_n.x * l.d.x + plan_n.y * l.d.y + plan_n.z * l.d.z)
 
    intersection = Point(l.p0.x + t * l.d.x, l.p0.y + t * l.d.y, l.p0.z + t * l.d.z)
    return intersection


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
    return Vector(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def plus_minus(x, y):
    '''
    Laver en sammenligning mellem to tal med en lille margin til afrundinger
    '''
    margin = 0.0000001
    if x >= y - margin and x <= y + margin:
        return True
    return False

def subtract(v1: Vector, v2: Vector) -> Vector:
    '''
    Trækker to vektorer fra hinanden og returnerer resultatet
    '''
    return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def dot(v1: Vector, v2: Vector) -> float:
    '''
    Returner prikproduktet mellem v1 og v2
    '''
    return v1.x * v2.x + v1.y * v2.y

def cross(v1: Vector, v2: Vector) -> Vector:
    '''
    Returnerer krydsproduktet mellem to vektorer
    '''
    x = v1.y * v2.z - v1.z * v2.y
    y = v1.z * v2.x - v1.x * v2.z
    z = v1.x * v2.y - v1.y * v2.x
    return Vector(x, y, z)

def angle(v1: Vector, v2: Vector):
    '''
    Returnerer vinklen mellem to vektorer
    '''
    if v1.length() > 0.000001 and v2.length() > 0.000001:
        return math.acos(dot(v1,v2)/(v1.length() * v2.length()))
    return None

def distance(p1: Point, p2: Point):
    '''
    Returnerer afstanden mellem to punkter
    '''
    return Vector.connect(p1, p2).length()

if __name__ == "__main__":
    #Her testes biblioteket, hvis det køres som main-program.
    #Hvis biblioteket i stedet importeres til et andet program, springes nedenstående kode over

    pass