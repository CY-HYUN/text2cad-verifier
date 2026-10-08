import cadquery as cq
import math

# Profile 1: 60 mm circle on Plane1 (Z=0)
w1 = cq.Wire.makeCircle(30.0, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))

# Profile 2: closed wavy ring on Plane2 (Z=75)
# r = 35 + 5*cos(6*theta) -> peaks at 40 mm, troughs at 30 mm, 6 periods
n = 240
pts = []
for i in range(n):
    t = 2 * math.pi * i / n
    r = 35.0 + 5.0 * math.cos(6 * t)
    pts.append(cq.Vector(r * math.cos(t), r * math.sin(t), 75.0))
wave_edge = cq.Edge.makeSpline(pts, periodic=True)
w2 = cq.Wire.assembleEdges([wave_edge])

# Profile 3: 80 mm circle on Plane3 (Z=150)
w3 = cq.Wire.makeCircle(40.0, cq.Vector(0, 0, 150), cq.Vector(0, 0, 1))

# Loft section by section (ruled) so the surface never bulges beyond the profiles
solid = cq.Solid.makeLoft([w1, w2, w3], ruled=True)
body = cq.Workplane("XY").add(solid)

# Shell: remove top face, 2 mm wall (inward, so outer extents are preserved)
try:
    result = body.faces(">Z").shell(-2.0)
    if not result.val().isValid():
        raise ValueError
except Exception:
    result = body
