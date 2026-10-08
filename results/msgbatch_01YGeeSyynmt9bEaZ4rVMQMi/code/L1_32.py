import cadquery as cq

L, W, H = 80.0, 50.0, 30.0
c = 10.0

box = cq.Workplane("XY").box(L, W, H, centered=False)

def tetra(p0, p1, p2, p3):
    pts = [cq.Vector(*p) for p in (p0, p1, p2, p3)]
    faces = []
    for tri in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]:
        w = cq.Wire.makePolygon([pts[i] for i in tri], close=True)
        faces.append(cq.Face.makeFromWires(w))
    sh = cq.Shell.makeShell(faces)
    return cq.Solid.makeSolid(sh)

# Upper left front corner (x=0, y=0, z=H)
t1 = tetra((0, 0, H), (c, 0, H), (0, c, H), (0, 0, H - c))
# Lower right rear corner (x=L, y=W, z=0)
t2 = tetra((L, W, 0), (L - c, W, 0), (L, W - c, 0), (L, W, c))

result = box.cut(cq.Workplane().add(t1)).cut(cq.Workplane().add(t2))
