import cadquery as cq

L, W, H = 80.0, 50.0, 30.0
c = 10.0

box = cq.Workplane("XY").box(L, W, H)

def tetra(p0, p1, p2, p3):
    pts = [cq.Vector(*p) for p in (p0, p1, p2, p3)]
    idx = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    faces = []
    for a, b, d in idx:
        w = cq.Wire.makePolygon([pts[a], pts[b], pts[d]], close=True)
        faces.append(cq.Face.makeFromWires(w))
    shell = cq.Shell.makeShell(faces)
    return cq.Solid.makeSolid(shell)

# Left front upper corner (x min, y min, z max)
x0, y0, z0 = -L / 2, -W / 2, H / 2
t1 = tetra((x0, y0, z0), (x0 + c, y0, z0), (x0, y0 + c, z0), (x0, y0, z0 - c))

# Right rear lower corner (x max, y max, z min)
x1, y1, z1 = L / 2, W / 2, -H / 2
t2 = tetra((x1, y1, z1), (x1 - c, y1, z1), (x1, y1 - c, z1), (x1, y1, z1 + c))

result = box.cut(cq.Workplane("XY").add(t1)).cut(cq.Workplane("XY").add(t2))
