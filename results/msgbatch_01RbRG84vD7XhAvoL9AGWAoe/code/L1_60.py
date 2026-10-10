import cadquery as cq
import math

# Base disk: diameter 100, thickness 12, extruded up from z=0
base = cq.Workplane("XY").circle(50).extrude(12)

# Four through-holes, diameter 10, on a 70 mm bolt circle at 0/90/180/270 degrees
pts = [(35, 0), (0, 35), (-35, 0), (0, -35)]
plate = base.faces(">Z").workplane().pushPoints(pts).hole(10)

# 0.8 mm 45-degree chamfer on the top edges of the holes
solid = plate.val()
top_edges = []
for e in solid.Edges():
    c = e.Center()
    bb = e.BoundingBox()
    if abs(bb.zmin - 12) < 1e-6 and abs(bb.zmax - 12) < 1e-6:
        # hole edges have radius 5 (bbox size ~10), skip the outer rim
        if bb.xlen < 20:
            top_edges.append(e)

result_shape = solid.chamfer(0.8, None, top_edges)
result = cq.Workplane("XY").newObject([result_shape])
