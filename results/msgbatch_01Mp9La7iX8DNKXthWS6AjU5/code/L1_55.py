import cadquery as cq
import math

pts = [(10, 0), (35, 0), (20, 60), (10, 60)]
body = (cq.Workplane("XZ")
        .polyline(pts).close()
        .revolve(360, (0, 0, 0), (0, 1, 0)))

def outer_bottom(edges):
    out = []
    for e in edges:
        bb = e.BoundingBox()
        if abs(bb.zmin) < 1e-6 and abs(bb.zmax) < 1e-6 and abs(bb.xlen - 70) < 1e-3:
            out.append(e)
    return out

sel = outer_bottom(body.edges().vals())
result = body.newObject(sel).chamfer(2.0)
