import cadquery as cq

cube = cq.Workplane("XY").rect(50, 50).extrude(50).translate((25, 25, 0))

A = cq.Vector(50, 50, 50)
B = cq.Vector(35, 50, 50)
C = cq.Vector(50, 35, 50)
D = cq.Vector(50, 50, 35)

def face(p, q, r):
    w = cq.Wire.makePolygon([p, q, r, p])
    return cq.Face.makeFromWires(w)

faces = [face(A, B, C), face(A, C, D), face(A, D, B), face(B, C, D)]
shell = cq.Shell.makeShell(faces)
tet = cq.Solid.makeSolid(shell)

result = cube.cut(cq.Workplane("XY").add(tet))
