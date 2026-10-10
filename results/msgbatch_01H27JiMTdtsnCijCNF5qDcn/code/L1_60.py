import cadquery as cq
import math

disk = cq.Workplane("XY").circle(50.0).extrude(12.0)

pts = [(35.0, 0), (-35.0, 0), (0, 35.0), (0, -35.0)]

body = (
    disk.faces(">Z").workplane()
    .pushPoints(pts)
    .hole(10.0)
)

# chamfer the hole edges on the top face
result = (
    body.faces(">Z").edges("%CIRCLE")
    .edges(cq.selectors.BoxSelector((-40, -40, 11.9), (40, 40, 12.1)))
    .chamfer(0.8)
)
