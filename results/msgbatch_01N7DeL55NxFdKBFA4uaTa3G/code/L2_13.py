import cadquery as cq
import math

R = 30.0                                   # circumscribed sphere radius
phi = (1 + math.sqrt(5)) / 2
a = 4 * R / (math.sqrt(3) * (1 + math.sqrt(5)))      # edge length
r_in = a / 2 * math.sqrt((25 + 11 * math.sqrt(5)) / 10)  # inradius
pent_inr = a / (2 * math.tan(math.radians(36)))        # pentagon inscribed circle radius
hole_r = pent_inr * 0.75                               # central circle on each face

# 6 symmetry axes through opposite face pairs (icosahedron vertex directions)
axes = [(0, 1, phi), (0, 1, -phi), (1, phi, 0), (1, -phi, 0), (phi, 0, 1), (-phi, 0, 1)]

def unit(v):
    l = math.sqrt(sum(c * c for c in v))
    return tuple(c / l for c in v)

def plane_for(n):
    n = unit(n)
    ref = (1, 0, 0) if abs(n[0]) < 0.9 else (0, 1, 0)
    x = (ref[1] * n[2] - ref[2] * n[1],
         ref[2] * n[0] - ref[0] * n[2],
         ref[0] * n[1] - ref[1] * n[0])
    return cq.Plane(origin=(0, 0, 0), xDir=unit(x), normal=n)

# Solid dodecahedron as intersection of 6 slabs
body = None
for n in axes:
    slab = cq.Workplane(plane_for(n)).box(4 * R, 4 * R, 2 * r_in)
    body = slab if body is None else body.intersect(slab)

# Cut a central circular hole through each pair of opposite faces (12 faces total)
for n in axes:
    cyl = cq.Workplane(plane_for(n)).circle(hole_r).extrude(2 * R, both=True)
    body = body.cut(cyl)

result = body
