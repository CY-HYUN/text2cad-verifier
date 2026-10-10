import cadquery as cq
import math

r = 15.0
L = 60.0
c = r * math.cos(math.radians(45))

profile = (
    cq.Workplane("XZ")
    .moveTo(0, r)
    .lineTo(L, r)
    .threePointArc((L + c, c), (L + r, 0))
    .lineTo(-r, 0)
    .threePointArc((-c, c), (0, r))
    .close()
)

result = profile.revolve(360, (0, 0, 0), (1, 0, 0))
