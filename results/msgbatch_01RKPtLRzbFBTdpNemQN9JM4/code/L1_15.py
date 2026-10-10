import cadquery as cq

cube = cq.Workplane("XY").box(50, 50, 50, centered=False)

B = cq.Vector(35, 50, 50)
C = cq.Vector(50, 35, 50)
D = cq.Vector(50, 50, 35)
E = cq.Vector(51, 51, 51)

def face(p, q, r):
    w = cq.Wire.makePolygon([p, q, r, p])
    return cq.Face.makeFromWires(w)

faces = [face(E, B, C), face(E, B, D), face(E, C, D), face(B, C, D)]
shell = cq.Shell.makeShell(faces)
tet = cq.Solid.makeSolid(shell)

result = cube.cut(cq.Workplane("XY").add(tet))
