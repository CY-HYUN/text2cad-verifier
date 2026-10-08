import cadquery as cq

L = 50.0
c = 15.0

cube = cq.Workplane("XY").box(L, L, L, centered=False)

# Tetrahedron that removes the corner at (L,L,L) using the plane x+y+z = 3L - c
s = 3 * L - c
m = L + 10.0  # extend beyond the cube to avoid coplanar faces
A = cq.Vector(m, m, m)
B = cq.Vector(s - 2 * m, m, m)
C = cq.Vector(m, s - 2 * m, m)
D = cq.Vector(m, m, s - 2 * m)

def tri(p1, p2, p3):
    return cq.Face.makeFromWires(cq.Wire.makePolygon([p1, p2, p3, p1]))

faces = [tri(B, C, D), tri(A, B, C), tri(A, C, D), tri(A, D, B)]
tet = cq.Solid.makeSolid(cq.Shell.makeShell(faces))

result = cube.cut(cq.Workplane("XY").add(tet))
