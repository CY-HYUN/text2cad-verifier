import cadquery as cq
import math

base = cq.Workplane("XY").circle(50).extrude(12)
pts = [(35, 0), (0, 35), (-35, 0), (0, -35)]
base = base.faces(">Z").workplane().pushPoints(pts).hole(10)

top_edges = base.faces(">Z").edges().vals()
hole_edges = [e for e in top_edges if abs(math.hypot(e.Center().x, e.Center().y) - 35) < 1e-3]

solid = base.val()
solid = solid.chamfer(0.8, 0.8, hole_edges)

result = cq.Workplane("XY").newObject([solid])
