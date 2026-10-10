import cadquery as cq
import math

thickness = 10.0
disc = cq.Workplane("XY").circle(50.0).extrude(thickness)

pts = [(35.0 * math.cos(math.radians(90 * i)), 35.0 * math.sin(math.radians(90 * i))) for i in range(4)]

holes = (
    cq.Workplane("XY")
    .pushPoints(pts)
    .circle(5.0)
    .extrude(thickness)
)

result = disc.cut(holes)
