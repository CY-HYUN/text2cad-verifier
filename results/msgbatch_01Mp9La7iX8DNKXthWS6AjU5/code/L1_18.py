import cadquery as cq
import math

r = 15.0
L = 60.0
s = math.sqrt(2) / 2

profile = (
    cq.Workplane("XZ")
    .moveTo(0, r)
    .lineTo(L, r)
    .threePointArc((L + r * s, r * s), (L + r, 0))
    .lineTo(-r, 0)
    .threePointArc((-r * s, r * s), (0, r))
    .close()
)

result = profile.revolve(360, (0, 0, 0), (1, 0, 0))
