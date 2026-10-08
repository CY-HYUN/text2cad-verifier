import cadquery as cq

# Cube: 50 mm square on XY plane (centered), extruded 50 mm in +Z
L = 50.0
d = 15.0
cube = cq.Workplane("XY").rect(L, L).extrude(L)

# Selected vertex (top corner at +X,+Y,+Z)
V = cq.Vector(L / 2, L / 2, L)
P1 = V - cq.Vector(d, 0, 0)
P2 = V - cq.Vector(0, d, 0)
P3 = V - cq.Vector(0, 0, d)

def tri(a, b, c):
    w = cq.Wire.makePolygon([a, b, c, a])
    return cq.Face.makeFromWires(w)

# Tetrahedron forming the corner outside the cutting plane P1-P2-P3
faces = [
    tri(P1, P2, P3),
    tri(V, P2, P1),
    tri(V, P3, P2),
    tri(V, P1, P3),
]
tetra = cq.Solid.makeSolid(cq.Shell.makeShell(faces))

result = cube.cut(cq.Workplane("XY").add(tetra))
