import cadquery as cq
import math

thickness = 10.0
disc = cq.Workplane("XY").circle(50.0).extrude(thickness)

pts = [(35.0 * math.cos(math.radians(a)), 35.0 * math.sin(math.radians(a))) for a in (0, 90, 180, 270)]
result = (
    disc.faces(">Z").workplane()
    .pushPoints(pts)
    .hole(10.0)
)
