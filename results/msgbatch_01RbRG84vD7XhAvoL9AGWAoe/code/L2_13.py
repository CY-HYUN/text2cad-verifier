import cadquery as cq
import math

phi = (1 + 5 ** 0.5) / 2
R = 30.0
s = R / math.sqrt(3)                     # scale for vertex set (±1,±1,±1)...
r_in = s * (1 + phi) / math.sqrt(1 + phi ** 2)   # inradius
a = s * 2 / phi                          # edge length
pent_in = a / (2 * math.tan(math.radians(36)))   # pentagon inradius

# Face normals (one per opposite pair)
normals = []
for (x, y, z) in [(0, phi, 1), (0, phi, -1)]:
    normals.append((x, y, z))
    normals.append((z, x, y))
    normals.append((y, z, x))

def unit(v):
    l = math.sqrt(sum(c * c for c in v))
    return tuple(c / l for c in v)

normals = [unit(n) for n in normals]

# Build dodecahedron as intersection of 6 slabs
solid = None
for n in normals:
    nv = cq.Vector(*n)
    slab = cq.Solid.makeCylinder(200, 2 * r_in, nv * (-r_in), nv)
    solid = slab if solid is None else solid.intersect(slab)

# Face-centre through holes (pairs of opposite faces)
hole_r = pent_in * 0.8
for n in normals:
    nv = cq.Vector(*n)
    cyl = cq.Solid.makeCylinder(hole_r, 4 * R, nv * (-2 * R), nv)
    solid = solid.cut(cyl)

result = cq.Workplane("XY").add(solid)
