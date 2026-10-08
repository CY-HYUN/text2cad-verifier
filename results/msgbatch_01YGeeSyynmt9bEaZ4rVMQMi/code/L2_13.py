import cadquery as cq
import math

R = 30.0  # circumscribed sphere radius
phi = (1 + math.sqrt(5)) / 2

# Edge length and inradius from circumradius
a = 4 * R / (math.sqrt(3) * (1 + math.sqrt(5)))
ri = a / 2 * math.sqrt((25 + 11 * math.sqrt(5)) / 10)
face_inr = a / (2 * math.tan(math.radians(36)))  # pentagon inscribed circle radius

# Face normal axes (6 axes -> 12 faces), icosahedron vertex directions
raw = [(0, 1, phi), (0, 1, -phi), (1, phi, 0), (1, -phi, 0), (phi, 0, 1), (-phi, 0, 1)]
axes = []
for v in raw:
    L = math.sqrt(sum(c * c for c in v))
    axes.append(cq.Vector(v[0] / L, v[1] / L, v[2] / L))

# Build the solid dodecahedron as intersection of 6 slabs
big = 4 * R
solid = None
for n in axes:
    slab = cq.Solid.makeCylinder(big, 2 * ri, n * (-ri), n)
    solid = slab if solid is None else solid.intersect(slab)

# Cut a central circular hole through each pair of opposite faces
hole_r = 0.8 * face_inr
for n in axes:
    cyl = cq.Solid.makeCylinder(hole_r, 4 * R, n * (-2 * R), n)
    solid = solid.cut(cyl)

result = cq.Workplane("XY").add(solid)
