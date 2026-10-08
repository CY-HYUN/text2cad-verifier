import cadquery as cq
import math

L = 60.0   # straight segment length
R = 15.0   # radius
h = L / 2.0
c = R * math.cos(math.radians(45))

result = (
    cq.Workplane("XZ")
    .moveTo(-h - R, 0)
    .lineTo(h + R, 0)
    .threePointArc((h + c, c), (h, R))
    .lineTo(-h, R)
    .threePointArc((-h - c, c), (-h - R, 0))
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0))
)
