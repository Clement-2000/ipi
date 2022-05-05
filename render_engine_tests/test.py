from ThreeDimensionnalSpace import *

reader = OBJReader()
cube = reader.readFile("cube.obj")
cube.transform = Transform(Point(0, 0, 0), Rotation(0, 0, 45), Scale(1, 1, 1))

for face in cube.get_faces(): 
    print(f"{round(face.point_a.x, 1)} {round(face.point_a.y, 1)} {round(face.point_a.z, 1)} - {round(face.point_b.x, 1)} {round(face.point_b.y, 1)} {round(face.point_b.z, 1)} - {round(face.point_c.x, 1)} {round(face.point_c.y, 1)} {round(face.point_c.z, 1)}")