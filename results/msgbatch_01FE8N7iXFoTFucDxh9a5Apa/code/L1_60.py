import cadquery as cq
import math

# Disk: 100 mm diameter, 12 mm thick, bottom face centred on the origin
disk = cq.Workplane("XY").circle(50).extrude(12)

# Four through-holes, 10 mm diameter, on a 70 mm bolt circle
pts = [(35, 0), (0, 35), (-35, 0), (0, -35)]
result = (
    disk.faces(">Z").workplane()
    .pushPoints(pts)
    .hole(10)
)

# 0.8 mm x 45 deg chamfer on the top edge of each hole
def is_hole_top_edge(e):
    c = e.Center()
    return abs(c.z - 12) < 1e-6 and math.hypot(c.x, c.y) < 45

hole_edges = [e for e in result.faces(">Z").edges().vals() if is_hole_top_edge(e)]
result = result.newObject(hole_edges).chamfer(0.8)
