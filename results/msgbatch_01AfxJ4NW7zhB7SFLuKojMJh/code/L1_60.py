import cadquery as cq
import math

disk = cq.Workplane("XY").circle(50).extrude(12)
pts = [(35, 0), (0, 35), (-35, 0), (0, -35)]
disk = disk.faces(">Z").workplane(origin=(0, 0, 12)).pushPoints(pts).hole(10)

# chamfer top edges of the holes
def hole_top_edge(e):
    c = e.Center()
    return abs(c.z - 12) < 1e-6 and e.radius() < 6 if e.geomType() == "CIRCLE" else False

edges = [e for e in disk.edges().vals() if e.geomType() == "CIRCLE" and abs(e.Center().z - 12) < 1e-6 and abs(e.radius() - 5) < 1e-6]
result = disk.newObject(edges).chamfer(0.8)
