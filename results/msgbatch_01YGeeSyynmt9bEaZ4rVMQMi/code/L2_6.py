import cadquery as cq
import math

# Cylinder: diameter 30, height 80
R = 15.0
H = 80.0
cylinder = cq.Workplane("XY").circle(R).extrude(H)

# Helix: pitch 20, 4 turns, on the cylinder surface starting at the end-face edge
pitch = 20.0
turns = 4
helix = cq.Wire.makeHelix(pitch=pitch, height=pitch * turns, radius=R)

# Semicircle profile (r=2) at helix start (15,0,0): flat edge on the cylinder
# surface, arc pointing inward. A small outward overshoot is added for a clean cut.
r = 2.0
eps = 0.3
profile = (
    cq.Workplane("XZ")
    .moveTo(R + eps, -r)
    .lineTo(R + eps, r)
    .lineTo(R, r)
    .threePointArc((R - r, 0), (R, -r))
    .close()
)

groove = profile.sweep(cq.Workplane(obj=helix), isFrenet=True)

result = cylinder.cut(groove)
