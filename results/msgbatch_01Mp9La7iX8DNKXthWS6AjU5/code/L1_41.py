import cadquery as cq
import math

disc = cq.Workplane("XY").circle(50.0).extrude(10.0)

pts = [(35.0 * math.cos(math.radians(a)), 35.0 * math.sin(math.radians(a))) for a in (0, 90, 180, 270)]

holes = (
    cq.Workplane("XY")
    .pushPoints(pts)
    .circle(5.0)
    .extrude(10.0)
)

result = disc.cut(holes)
