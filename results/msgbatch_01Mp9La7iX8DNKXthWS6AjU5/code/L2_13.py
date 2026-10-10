import cadquery as cq
import math

phi = (1 + 5 ** 0.5) / 2
s = 30.0 / math.sqrt(3)

# dodecahedron vertices (circumradius 30)
verts = []
for x in (-1, 1):
    for y in (-1, 1):
        for z in (-1, 1):
            verts.append((x, y, z))
for a in (-1, 1):
    for b in (-1, 1):
        verts.append((0, a / phi, b * phi))
        verts.append((a / phi, b * phi, 0))
        verts.append((a * phi, 0, b / phi))
verts = [(x * s, y * s, z * s) for x, y, z in verts]

# face normals (icosahedron vertex directions)
normals = []
for a in (-1, 1):
    for b in (-1, 1):
        normals.append((0, a * phi, b * 1.0))
        normals.append((a * 1.0, 0, b * phi))
        normals.append((a * phi, b * 1.0, 0))


def norm(v):
    l = math.sqrt(sum(c * c for c in v))
    return tuple(c / l for c in v)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


faces = []
for n in normals:
    nn = norm(n)
    ds = sorted(verts, key=lambda v: -dot(v, nn))
    pts = ds[:5]
    ref = (0, 0, 1) if abs(nn[2]) < 0.9 else (1, 0, 0)
    u = norm(cross(nn, ref))
    w = cross(nn, u)
    c = tuple(sum(p[i] for p in pts) / 5 for i in range(3))
    pts.sort(key=lambda p: math.atan2(dot(tuple(p[i] - c[i] for i in range(3)), w),
                                      dot(tuple(p[i] - c[i] for i in range(3)), u)))
    vs = [cq.Vector(*p) for p in pts]
    wire = cq.Wire.makePolygon(vs + [vs[0]])
    faces.append(cq.Face.makeFromWires(wire))

shell = cq.Shell.makeShell(faces)
solid = cq.Solid.makeSolid(shell)
body = cq.Workplane("XY").add(solid)
if solid.Volume() < 0:
    solid = cq.Solid(solid.wrapped.Reversed())
    body = cq.Workplane("XY").add(solid)

# circular holes from every face center toward / through the center
r_hole = 12.5
for n in normals:
    nn = norm(n)
    cyl = cq.Solid.makeCylinder(r_hole, 40, cq.Vector(0, 0, 0), cq.Vector(*nn))
    body = body.cut(cq.Workplane("XY").add(cyl))

result = body
