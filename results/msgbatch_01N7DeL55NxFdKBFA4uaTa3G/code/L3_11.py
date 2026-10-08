import cadquery as cq
import math

# Guide curve: cubic Bezier in XZ plane
pts = [cq.Vector(0, 0, 0), cq.Vector(0, 0, 60), cq.Vector(60, 0, 60), cq.Vector(60, 0, 120)]
try:
    path_edge = cq.Edge.makeBezier(pts)
except Exception:
    path_edge = cq.Edge.makeSpline(pts[::3], tangents=[cq.Vector(0, 0, 1), cq.Vector(0, 0, 1)])
path = cq.Wire.assembleEdges([path_edge])

# End tangent of Bezier = P3 - P2
tan = (pts[3] - pts[2]).normalized()
top_plane = cq.Plane(origin=pts[3], xDir=cq.Vector(1, 0, 0) if abs(tan.x) < 0.9 else cq.Vector(0, 1, 0), normal=tan)

def section(a, b, r):
    w1 = cq.Workplane("XY").ellipse(a, b).val()
    w2 = cq.Workplane(top_plane).circle(r).val()
    return cq.Solid.sweep_multi([w1, w2], path, makeSolid=True, isFrenet=False)

t = 3.0
outer = section(60, 40, 30)
inner = section(60 - t, 40 - t, 30 - t)

body = cq.Workplane("XY").add(outer).cut(cq.Workplane("XY").add(inner))

# Top flange: ring from inner hole (D54) to D70, 2 mm outward along normal
flange = (
    cq.Workplane(top_plane)
    .circle(35.0)
    .circle(30.0 - t)
    .extrude(2.0)
)

result = body.union(flange)
