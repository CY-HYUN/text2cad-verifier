import cadquery as cq
import math

cyl = cq.Workplane("XY").circle(30.0).extrude(80.0)

profile = (
    cq.Workplane("XZ")
    .polyline([(27, 35), (30, 35), (30, 45), (27, 45)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
# make the cutter slightly larger radially to ensure clean cut through the outer surface
cutter = (
    cq.Workplane("XZ")
    .polyline([(27, 35), (31, 35), (31, 45), (27, 45)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

body = cyl.cut(cutter)

def outer_groove_edge(e):
    c = e.Center()
    bb = e.BoundingBox()
    return (abs(bb.xmax - 30.0) < 1e-3 and (abs(c.z - 35.0) < 1e-3 or abs(c.z - 45.0) < 1e-3)
            and abs(bb.zmax - bb.zmin) < 1e-6)

edges = [e for e in body.edges().vals() if outer_groove_edge(e)]

solid = body.val().fillet(1.0, edges)
result = cq.Workplane("XY").newObject([solid])
