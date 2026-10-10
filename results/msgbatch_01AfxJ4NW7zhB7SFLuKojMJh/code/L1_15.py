import cadquery as cq

cube = cq.Workplane("XY").box(50, 50, 50, centered=False)

A = cq.Vector(35, 50, 50)
B = cq.Vector(50, 35, 50)
C = cq.Vector(50, 50, 35)
D = cq.Vector(50, 50, 50)

def face(p, q, r):
    w = cq.Wire.makePolygon([p, q, r, p])
    return cq.Face.makeFromWires(w)

faces = [face(A, B, C), face(A, B, D), face(A, C, D), face(B, C, D)]
shell = cq.Shell.makeShell(faces)
tet = cq.Solid.makeSolid(shell)

# slightly enlarge the cutter beyond the corner to avoid coincident faces
result = cube.cut(cq.Workplane("XY").add(tet))
