import cadquery as cq

def tetra(p, d1, d2, d3, s=10.0):
    pts = [cq.Vector(*p)]
    for d in (d1, d2, d3):
        pts.append(cq.Vector(p[0] + s * d[0], p[1] + s * d[1], p[2] + s * d[2]))
    faces = []
    for idx in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]:
        w = cq.Wire.makePolygon([pts[i] for i in idx], close=True)
        faces.append(cq.Face.makeFromWires(w))
    sh = cq.Shell.makeShell(faces)
    return cq.Solid.makeSolid(sh)

body = cq.Workplane("XY").box(80, 50, 30, centered=False)

t1 = tetra((0, 0, 30), (1, 0, 0), (0, 1, 0), (0, 0, -1))
t2 = tetra((80, 50, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 1))

result = body.cut(cq.Workplane("XY").add(t1)).cut(cq.Workplane("XY").add(t2))
