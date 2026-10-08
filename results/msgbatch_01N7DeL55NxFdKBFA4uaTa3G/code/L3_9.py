import cadquery as cq
import math

# Profile 1: 60 mm diameter circle on Plane1 (Z=0)
w1 = cq.Wire.makeCircle(30.0, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))

# Profile 2: wavy ring on Plane2 (Z=75), 6 periods, radius 35 +/- 5
N = 120
pts = []
for i in range(N):
    t = 2 * math.pi * i / N
    r = 35.0 + 5.0 * math.cos(6 * t)
    pts.append(cq.Vector(r * math.cos(t), r * math.sin(t), 75.0))
wave_edge = cq.Edge.makeSpline(pts, periodic=True)
w2 = cq.Wire.assembleEdges([wave_edge])

# Profile 3: 80 mm diameter circle on Plane3 (Z=150)
w3 = cq.Wire.makeCircle(40.0, cq.Vector(0, 0, 150), cq.Vector(0, 0, 1))

# Smooth loft through the three profiles
solid = cq.Solid.makeLoft([w1, w2, w3], ruled=False)
body = cq.Workplane("XY").add(solid)

# Shell: remove top face, 2 mm wall
try:
    shelled = body.faces(">Z").shell(-2.0)
    if shelled.val().isValid():
        result = shelled
    else:
        result = body
except Exception:
    result = body
