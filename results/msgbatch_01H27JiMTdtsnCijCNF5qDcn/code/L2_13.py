import cadquery as cq
import math

R = 30.0
phi = (1 + math.sqrt(5)) / 2
ri = R * 0.7946544723  # inradius of dodecahedron with circumradius R
edge = R * 0.7136441795
apothem = edge / (2 * math.tan(math.radians(36)))
r_hole = apothem * 0.92

# 12 face normals (icosahedron vertex directions)
normals = []
for s1 in (1, -1):
    for s2 in (1, -1):
        normals.append((0, s1 * 1, s2 * phi))
        normals.append((s1 * 1, s2 * phi, 0))
        normals.append((s2 * phi, 0, s1 * 1))

def unit(v):
    l = math.sqrt(sum(c * c for c in v))
    return (v[0] / l, v[1] / l, v[2] / l)

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def make_plane(origin, n):
    n = unit(n)
    ref = (1, 0, 0) if abs(n[0]) < 0.8 else (0, 1, 0)
    x = unit(cross(ref, n))
    return cq.Plane(origin=origin, xDir=x, normal=n)

# Build dodecahedron by cutting a large box with planes
body = cq.Workplane("XY").box(200, 200, 200)
for n in normals:
    u = unit(n)
    o = (u[0] * ri, u[1] * ri, u[2] * ri)
    pl = make_plane(o, u)
    cutter = cq.Workplane(pl).rect(400, 400).extrude(200)
    body = body.cut(cutter)

# Circular holes through the center along each of the 6 distinct face axes
# (each through-cut covers a face and its opposite face)
axes = []
for n in normals:
    u = unit(n)
    if not any(abs(u[0]+a[0]) < 1e-6 and abs(u[1]+a[1]) < 1e-6 and abs(u[2]+a[2]) < 1e-6 for a in axes):
        axes.append(u)

for u in axes:
    pl = make_plane((0, 0, 0), u)
    hole = cq.Workplane(pl).circle(r_hole).extrude(40, both=True)
    body = body.cut(hole)

result = body
