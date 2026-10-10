import cadquery as cq
import math

# Section profile (half, x >= 0) on the front (XZ) plane, revolved about the Z axis.
# Outer rectangle: 20 wide (radius) x 60 tall; spherical cavity R15 centred at z=30;
# 5 mm wide (radius 2.5) passage at the top; bottom closed.
cz = 30.0
R = 15.0
w = 2.5
zt = cz + math.sqrt(R**2 - w**2)

profile = (
    cq.Workplane("XZ")
    .moveTo(w, 60)
    .lineTo(20, 60)
    .lineTo(20, 0)
    .lineTo(0, 0)
    .lineTo(0, cz - R)
    .threePointArc((R, cz), (w, zt))
    .close()
)

result = profile.revolve(360, (0, 0, 0), (0, 1, 0))
