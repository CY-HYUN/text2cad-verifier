import cadquery as cq

box = cq.Workplane("XY").rect(80.0, 50.0, centered=False).extrude(30.0)

def tetra(c, p1, p2, p3):
    def face(a, b, d):
        w = cq.Wire.makePolygon([cq.Vector(*a), cq.Vector(*b), cq.Vector(*d), cq.Vector(*a)])
        return cq.Face.makeFromWires(w)
    faces = [face(c, p1, p2), face(c, p2, p3), face(c, p3, p1), face(p1, p2, p3)]
    return cq.Solid.makeSolid(cq.Shell.makeShell(faces))

# upper left front corner (0,0,30)
t1 = tetra((0, 0, 30), (10, 0, 30), (0, 10, 30), (0, 0, 20))
# lower right rear corner (80,50,0)
t2 = tetra((80, 50, 0), (70, 50, 0), (80, 40, 0), (80, 50, 10))

result = box.cut(cq.Workplane("XY").add(t1)).cut(cq.Workplane("XY").add(t2))
