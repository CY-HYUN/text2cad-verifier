import cadquery as cq
import math

def tetra(p0, p1, p2, p3):
    pts = [cq.Vector(*p) for p in (p0, p1, p2, p3)]
    idx = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    faces = []
    for a, b, c in idx:
        w = cq.Wire.makePolygon([pts[a], pts[b], pts[c], pts[a]])
        faces.append(cq.Face.makeFromWires(w))
    sh = cq.Shell.makeShell(faces)
    return cq.Solid.makeSolid(sh).fix()

block = cq.Workplane("XY").box(80, 50, 30, centered=False)

t1 = tetra((0, 0, 30), (10, 0, 30), (0, 10, 30), (0, 0, 20))
t2 = tetra((80, 50, 0), (70, 50, 0), (80, 40, 0), (80, 50, 10))

# expand slightly beyond the corner for a clean cut: use the exact tetrahedra
result = block.cut(cq.Workplane("XY").add(t1)).cut(cq.Workplane("XY").add(t2))
