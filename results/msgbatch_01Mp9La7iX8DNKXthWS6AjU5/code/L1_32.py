import cadquery as cq

box = cq.Workplane("XY").rect(80.0, 50.0).extrude(30.0)
box = box.translate((40, 25, 0))  # rectangle corner at the origin, x 0..80, y 0..50

def tetra(p0, p1, p2, p3):
    def face(a, b, c):
        pts = [cq.Vector(*a), cq.Vector(*b), cq.Vector(*c), cq.Vector(*a)]
        return cq.Face.makeFromWires(cq.Wire.makePolygon(pts))
    faces = [face(p0, p1, p2), face(p0, p1, p3), face(p0, p2, p3), face(p1, p2, p3)]
    return cq.Solid.makeSolid(cq.Shell.makeShell(faces))

def make(c, a, b, d):
    s = tetra(c, a, b, d)
    if s.Volume() < 0:
        s = tetra(c, b, a, d)
    return s

# upper left front corner (0,0,30)
t1 = make((0, 0, 30), (10, 0, 30), (0, 10, 30), (0, 0, 20))
# lower right rear corner (80,50,0)
t2 = make((80, 50, 0), (70, 50, 0), (80, 40, 0), (80, 50, 10))

result = box.cut(cq.Workplane("XY").add(t1)).cut(cq.Workplane("XY").add(t2))
