import cadquery as cq
import math

R = 15.0
L = 60.0
h = L / 2.0
c = R * math.cos(math.radians(45))

profile = (
    cq.Workplane("XZ")
    .moveTo(-h - R, 0)
    .threePointArc((-h - c, c), (-h, R))
    .lineTo(h, R)
    .threePointArc((h + c, c), (h + R, 0))
    .close()
)

result = profile.revolve(360, (0, 0, 0), (1, 0, 0))
