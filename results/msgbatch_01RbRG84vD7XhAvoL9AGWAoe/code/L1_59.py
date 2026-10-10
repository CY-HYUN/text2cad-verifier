import cadquery as cq
import math

# Base cylinder
cyl = cq.Workplane("XY").circle(30).extrude(80)

# Groove ring to cut (from r=27 to r=31, z=35..45)
ring = (
    cq.Workplane("XY")
    .workplane(offset=35)
    .circle(31)
    .circle(27)
    .extrude(10)
)

body = cyl.cut(ring)
solid = body.val()

# Select the outer groove edges (radius 30 circles at z=35 and z=45)
edges = []
for e in solid.Edges():
    c = e.Center()
    if e.geomType() == "CIRCLE":
        r = e.radius()
        bb = e.BoundingBox()
        z = bb.zmin
        if abs(r - 30) < 1e-3 and (abs(z - 35) < 1e-3 or abs(z - 45) < 1e-3):
            edges.append(e)

filleted = solid.fillet(1.0, edges)
result = cq.Workplane("XY").newObject([filleted])
