import cadquery as cq
import math

phi = (1 + math.sqrt(5)) / 2
R = 30.0
s = R / math.sqrt(3)

# dodecahedron vertices
base = []
for x in (-1, 1):
    for y in (-1, 1):
        for z in (-1, 1):
            base.append((x, y, z))
for a in (-1, 1):
    for b in (-1, 1):
        base.append((0, a / phi, b * phi))
        base.append((a / phi, b * phi, 0))
        base.append((b * phi, 0, a / phi))
verts = [cq.Vector(v[0] * s, v[1] * s, v[2] * s) for v in base]

# candidate normals
cands = []
for a in (-1, 1):
    for b in (-1, 1):
        for (p, q) in ((1, phi), (phi, 1)):
            cands.append((0, a * p, b * q))
            cands.append((a * p, b * q, 0))
            cands.append((b * q, 0, a * p))

faces = []
normals = []
for c in cands:
    n = cq.Vector(*c).normalized()
    ds = [v.dot(n) for v in verts]
    m = max(ds)
    idx = [i for i, d in enumerate(ds) if abs(d - m) < 1e-6]
    if len(idx) != 5:
        continue
    pts = [verts[i] for i in idx]
    cen = cq.Vector(0, 0, 0)
    for p in pts:
        cen = cen + p
    cen = cen * (1 / 5.0)
    # local basis
    ref = cq.Vector(1, 0, 0) if abs(n.x) < 0.9 else cq.Vector(0, 1, 0)
    u = ref.cross(n).normalized()
    w = n.cross(u)
    pts.sort(key=lambda p: math.atan2((p - cen).dot(w), (p - cen).dot(u)))
    wire = cq.Wire.makePolygon(pts + [pts[0]])
    faces.append(cq.Face.makeFromWires(wire))
    normals.append(n)

shell = cq.Shell.makeShell(faces)
solid = cq.Solid.makeSolid(shell)
body = cq.Workplane("XY").add(solid)

# unique axes
axes = []
for n in normals:
    if not any(abs(n.dot(a) ) > 0.999 for a in axes):
        axes.append(n)

hole_r = 12.0
for n in axes:
    cyl = cq.Solid.makeCylinder(hole_r, 80, cq.Vector(-n.x * 40, -n.y * 40, -n.z * 40), n)
    body = body.cut(cq.Workplane("XY").add(cyl))

result = body
