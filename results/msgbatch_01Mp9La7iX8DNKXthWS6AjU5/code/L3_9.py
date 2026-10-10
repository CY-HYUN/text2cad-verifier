import cadquery as cq
import math

# Datum plane heights
z1, z2, z3 = 0.0, 75.0, 150.0

# Bottom circle: 60 mm diameter on Plane1
w1 = cq.Wire.makeCircle(30.0, cq.Vector(0, 0, z1), cq.Vector(0, 0, 1))

# Middle wavy ring on Plane2: radius 35 +/- 5, 6 periods (peaks 40, troughs 30)
n_per = 8
n = 6 * n_per
pts = []
for i in range(n):
    t = 2 * math.pi * i / n
    r = 35.0 + 5.0 * math.cos(6 * t)
    pts.append(cq.Vector(r * math.cos(t), r * math.sin(t), z2))
wavy_edge = cq.Edge.makeSpline(pts, periodic=True)
w2 = cq.Wire.assembleEdges([wavy_edge])

# Top circle: 80 mm diameter on Plane3
w3 = cq.Wire.makeCircle(40.0, cq.Vector(0, 0, z3), cq.Vector(0, 0, 1))

# Smooth loft through the three profiles
solid = cq.Solid.makeLoft([w1, w2, w3], False)

# Shell: remove top face, 2 mm wall thickness (inward)
result = cq.Workplane("XY").newObject([solid]).faces(">Z").shell(-2.0)
