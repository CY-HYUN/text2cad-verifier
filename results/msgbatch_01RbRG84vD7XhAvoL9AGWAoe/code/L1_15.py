import cadquery as cq

L = 50.0
c = 15.0

cube = cq.Workplane("XY").box(L, L, L, centered=False)

# Corner at (L, L, L); cut plane through points 15 mm back along each edge
p1 = cq.Vector(L - c, L, L)
p2 = cq.Vector(L, L - c, L)
p3 = cq.Vector(L, L, L - c)
p0 = cq.Vector(L, L, L)

tet = cq.Solid.makeSolid(
    cq.Shell.makeShell([
        cq.Face.makeFromWires(cq.Wire.makePolygon([p1, p2, p3], close=True)),
        cq.Face.makeFromWires(cq.Wire.makePolygon([p0, p1, p2], close=True)),
        cq.Face.makeFromWires(cq.Wire.makePolygon([p0, p2, p3], close=True)),
        cq.Face.makeFromWires(cq.Wire.makePolygon([p0, p3, p1], close=True)),
    ])
)

result = cube.cut(cq.Workplane("XY").add(tet))
