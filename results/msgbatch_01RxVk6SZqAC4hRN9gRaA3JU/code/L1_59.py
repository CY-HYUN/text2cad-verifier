import cadquery as cq

# Base cylinder: diameter 60, height 80
body = cq.Workplane("XY").circle(30.0).extrude(80.0)

# Groove profile on XZ plane (local x = radial X, local y = global Z)
groove = (
    cq.Workplane("XZ")
    .polyline([(27.0, 35.0), (30.0, 35.0), (30.0, 45.0), (27.0, 45.0)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

body = body.cut(groove)

# Fillet the outer circular edges on both sides of the groove (r=30 at z=35 and z=45)
solid = body.val()
edges = []
for e in solid.Edges():
    if e.geomType() == "CIRCLE":
        try:
            r = e.radius()
        except Exception:
            continue
        z = e.Center().z
        if abs(r - 30.0) < 1e-3 and 34.0 < z < 46.0:
            edges.append(e)

if edges:
    solid = solid.fillet(1.0, edges)

result = cq.Workplane("XY").newObject([solid])
