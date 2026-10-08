import cadquery as cq
import math

R = 30.0
H = 80.0
groove_depth = 3.0
z0, z1 = 35.0, 45.0

# Base cylinder
cyl = cq.Workplane("XY").circle(R).extrude(H)

# Groove profile on XZ plane (local x = X radial, local y = Z), revolved around Z axis
groove = (
    cq.Workplane("XZ")
    .moveTo(R - groove_depth, z0)
    .lineTo(R + 0.5, z0)
    .lineTo(R + 0.5, z1)
    .lineTo(R - groove_depth, z1)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

body = cyl.cut(groove)
solid = body.val()

# Select circular edges at outer radius on both sides of the groove
edges = []
for e in solid.Edges():
    if e.geomType() == "CIRCLE":
        try:
            r = e.radius()
        except Exception:
            continue
        zc = e.Center().z
        if abs(r - R) < 1e-3 and (abs(zc - z0) < 1e-3 or abs(zc - z1) < 1e-3):
            edges.append(e)

if edges:
    solid = solid.fillet(1.0, edges)

result = cq.Workplane("XY").add(solid)
