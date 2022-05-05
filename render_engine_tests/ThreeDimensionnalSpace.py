from math import radians, cos, sin

class Point():
    def __init__(self, x , y, z) :
        assert type(x) in (int, float)
        assert type(y) in (int, float)
        assert type(z) in (int, float)

        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def is_confunded(a, b) :
        assert type(a) == Point
        assert type(b) == Point

        return a == b or\
               a.x == b.x and a.y == b.y and a.z == b.z
    
    @staticmethod
    def translate_point(point, translation) :
        assert type(point) == Point
        assert type(translation) == Point

        return Point(
            point.x + translation.x, 
            point.y + translation.y, 
            point.z + translation.z
        )

class Segment() :
    def __init__(self, start, end = None) :
        assert type(start) == Point
        assert type(end) in (Point, None)

        if end == None :
            self.start = Point(0, 0, 0)
            self.end = start
        else :
            self.start = start
            self.end = end

    def get_vector(self) :
        return Point(
            self.end.x - self.start.x, 
            self.end.y - self.start.y,
            self.end.z - self.start.z
        )

    def is_vector_colinear(a, b) :
        assert type(a) == Segment
        assert type(b) == Segment

        vec_a = a.get_vector()
        vec_b = b.get_vector()

        return vec_a.x*vec_b.x == vec_b.x*vec_a.x and\
               vec_a.y*vec_b.x == vec_b.y*vec_a.x and\
               vec_a.z*vec_b.x == vec_b.z*vec_a.x

    @staticmethod
    def vector_add(a, b) :
        assert type(a) == Segment
        assert type(b) == Segment

        vec_a = a.get_vec()
        vec_b = b.get_vec()

        return Segment(Point(vec_a.x + vec_b.x, vec_a.y + vec_b.y, vec_a.z + vec_b.z))

    @staticmethod
    def vector_multiply(a, b) :
        assert type(a) in (Segment, int, float)
        assert type(b) == Segment

        vec_b = b.get_vec()

        if type(a) == Segment :
            vec_a = a.get_vec()

            return Segment(Point(
                vec_a.x*vec_b.x,
                vec_a.y*vec_b.y,
                vec_a.z*vec_b.z
            ))

        return Segment(Point(
            a*vec_b.x,
            a*vec_b.y,
            a*vec_b.z
        ))

    @staticmethod
    def vector_scalar_product(a, b) :
        assert type(a) == Segment
        assert type(b) == Segment

        vec_a = a.get_vec()
        vec_b = b.get_vec()

        return vec_a.x * vec_b.x + vec_a.y * vec_a.y + vec_a.z * vec_a.z

    @staticmethod
    def vector_vectorial_product(a, b) :
        assert type(a) == Segment
        assert type(b) == Segment

        vec_a = a.get_vec()
        vec_b = b.get_vec()

        return Segment(
            vec_a.y * vec_b.z - vec_a.y * vec_b.z,
            vec_a.z * vec_b.x - vec_a.z * vec_b.x,
            vec_a.x * vec_b.y - vec_a.x * vec_b.y,
        )

    @staticmethod
    def get_common_point(a, b) :
        assert type(a) == Segment
        assert type(b) == Segment

        if Point.is_confunded(a.start, b.start) or Point.is_confunded(a.start, b.end) :
            return a.start
        elif Point.is_confunded(a.end, b.end) or Point.is_confunded(a.end, b.start) :
            return a.end

        return None

class Face() :
    def __init__(self, normal, segment_b = None, point_c = None) :
        assert (type(normal), type(segment_b), type(point_c)) == (Segment, None, None) or\
               (type(normal), type(segment_b), type(point_c)) == (Segment, Segment, None) or\
               (type(normal), type(segment_b), type(point_c)) == (Point, Point, Point)

        if segment_b == point_c == None :
            normal_vec = normal.get_vector(normal)

            if normal_vec.z == 0 :
                normal_vec.z = 1

            self.point_a = Point(normal.start.x, normal.start.y, normal.start.z)
            self.point_b = Point(normal.start.x + 1, normal_vec.start.y, normal.start.z - normal_vec.y / normal_vec.z)
            self.point_c = Point(normal.start.x, normal_vec.start.y + 1, normal.start.z - normal_vec.x / normal_vec.z)

        elif segment_b == None :
            assert not Segment.is_vec_colinear(normal, segment_b)

            if Segment.get_common_point(normal, segment_b) :
                self.point_a = Segment.get_common_point(normal, segment_b)

                if Point.is_confunded(self.point_a, normal.start) :
                    self.point_b = normal.end
                else :
                    self.point_b = normal.start

                if Point.is_confunded(self.point_a, segment_b.start) :
                    self.point_c = segment_b.end
                else :
                    self.point_c = segment_b.start

        else :
            self.point_a = normal
            self.point_b = segment_b
            self.point_c = point_c

    def get_normal(self) :
        return Segment.vector_scalar_product(self.segment_a, self.segment_b)

class Rotation() :
    def __init__(self, x, y, z) :
        assert type(x) in (int, float)
        assert type(y) in (int, float)
        assert type(z) in (int, float)

        self.x = x % 360
        self.y = y % 360
        self.z = z % 360
    
    @staticmethod
    def rotate_point(point, rotation): 
        assert type(point) == Point
        assert type(rotation) == Rotation

        x = point.x
        y = point.y
        z = point.z

        cx = cos(radians(rotation.x))
        cy = cos(radians(rotation.y))
        cz = cos(radians(rotation.z))
        sx = sin(radians(rotation.x))
        sy = sin(radians(rotation.y))
        sz = sin(radians(rotation.z))

        x =           (cy*cz)*x +          (-cy*sz)*y +     (sy)*z
        y =  (sx*sy*cz+cx*sz)*x + (-sx*sy*sz+cx*cz)*y + (-sx*cy)*z
        z = (-cx*sy*cz+sx*sz)*x +  (cx*sy*sz+sx*cz)*y +  (cx*cy)*z

        return Point(x, y, z)

class Scale():
    def __init__(self, x, y, z) : 
        assert type(x) in (int, float)
        assert type(y) in (int, float)
        assert type(z) in (int, float)

        self.x = x
        self.y = y
        self.z = z
    
    @staticmethod
    def scale_point(point, scale) : 
        assert type(point) == Point
        assert type(scale) == Scale

        return Point(
            point.x * scale.x,
            point.y * scale.y,
            point.z * scale.z
        )
        
class Transform() :
    def __init__(self, point, rotation, scale) :
        assert type(point) == Point
        assert type(rotation) == Rotation
        assert type(scale) == Scale

        self.point = point
        self.rotation = rotation
        self.scale = scale
    
    @staticmethod
    def transform_point(point, transform) : 
        assert type(point) == Point
        assert type(transform) == Transform

        return Point.translate_point(Rotation.rotate_point(Scale.scale_point(point, transform.scale), transform.rotation), transform.point)

class Object() :
    def __init__(self, transform = Transform(Point(0, 0, 0), Rotation(0, 0, 0), Scale(1, 1, 1))) :
        assert type(transform) == Transform

        self.display = False
        self.transform = transform
        self.faces = []

    def addMesh(self, faces) :
        assert type(faces) in (list, tuple)

        for face in faces :
            self.faces.append(face)

    def set_display_state(self, state) : 
        assert type(state) == bool

        self.display = state
    
    def get_faces(self):
        faces = []
        for face in self.faces : 
            
            faces.append(Face(
                Transform.transform_point(face.point_a, self.transform),
                Transform.transform_point(face.point_b, self.transform),
                Transform.transform_point(face.point_c, self.transform)
            ))
        
        return faces

class OBJReader() : 
    @staticmethod
    def readFile(path): 
        points = []
        faces = []

        file = open(path)
        
        lines = list(filter(None, file.read().split("\n")))

        for line in lines : 
            elements = list(filter(None, line.split(" ")))

            t = elements.pop(0)

            if t == "v" and len(elements) == 3 : 
                x = float(elements[0])
                y = float(elements[1])
                z = float(elements[2])

                points.append(Point(x, y, z))
            
            elif t == "f" : 
                point_a_index = int(elements[0])-1
                point_b_index = int(elements[1])-1
                point_c_index = int(elements[2])-1

                faces.append(Face(
                    points[point_a_index],
                    points[point_b_index],
                    points[point_c_index]
                ))
        
        o = Object()
        o.addMesh(faces)

        return o

    def makeObj(object) : 
        return 

class Group() :
    def __init__(self, transform = Transform(Point(0, 0, 0), Rotation(0, 0, 0), Scale(1, 1, 1))) :
        self.objects = []
        self.transform = transform
    
    def addObject(self, object) : 
        self.objects.append(object)

class Sensor():
    def __init__(self, sensor_width, sensor_height, focal_length):
        assert type(sensor_width) == int and sensor_width > 0
        assert type(sensor_height) == int and sensor_height > 0
        assert type(focal_length) in (int, float) and focal_length > 0

        self.sensor_width = sensor_width
        self. sensor_height = sensor_height
        self.focal_length = focal_length

class Camera():
    def __init__(self, transform, sensor): 
        assert type(transform) == Transform
        assert type(sensor) == Sensor

        self.transform = transform
        self.sensor = sensor
    
    def move(self, transform):
        assert type(transform) == Transform

        self.transform = transform
    
    def rotate(self, rot):
        assert type(rot) == Rotation

        self.rot = rot
    
    def get_plane_center_point(self):
        return Point(
            self.pos.x + self.sensor.focal_length * cos(radians(self.rot.z)),
            self.pos.y + self.sensor.focal_length * sin(radians(self.rot.z)),
            0
        )

class World() :
    def __init__(self) :
        self.objects = []
        self.groups = []
        self.cameras = [Camera(Transform(Point(0, 0, 0), Rotation(0, 0, 0), Scale(1, 1, 1)), Sensor(36, 24, 50))]
        self.active_camera = 0
    
    def addObject(self, object) : 
        self.objects.append(object)
    
    def addGroup(self, group) : 
        self.groups.append(group)
    
    def addCamera(self, camera) : 
        self.cameras.append(camera)
    
    def setActiveCamera(self, index) : 
        assert type(index) == int
        self.active_camera = index
