import cadquery as cq
import math

cube = cq.Workplane("XY").rect(50, 50).extrude(50)
cube = cube.translate((25, 25, 0))  # square spans 0..50 in X and Y

n = cq.Vector(1, 1, 1).normalized()
d = 15 / math.sqrt(3)
h = 100
center = n * (d - h / 2)

plane = cq.Plane(origin=(center.x, center.y, center.z), xDir=(1, -1, 0), normal=(n.x, n.y, n.z))
cutter = cq.Workplane(plane).rect(300, 300).extrude(h / 2, both=True)

result = cube.cut(cutter)
