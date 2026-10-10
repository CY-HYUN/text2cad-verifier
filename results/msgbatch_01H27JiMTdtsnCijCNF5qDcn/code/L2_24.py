import cadquery as cq
import math

R = 15.0
cz = 30.0
hw = 2.5
zt = cz + math.sqrt(R**2 - hw**2)

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(20, 0)
    .lineTo(20, 60)
    .lineTo(hw, 60)
    .lineTo(hw, zt)
    .threePointArc((R, cz), (0, cz - R))
    .close()
)

result = profile.revolve(360, (0, 0, 0), (0, 1, 0))
