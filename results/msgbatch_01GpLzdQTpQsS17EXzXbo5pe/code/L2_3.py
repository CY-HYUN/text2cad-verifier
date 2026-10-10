import cadquery as cq
import math

R = 40
# Semicircle on the front plane (XZ), straight edge at top (z=0), arc below
profile = (cq.Workplane("XZ")
           .moveTo(-R, 0).lineTo(R, 0)
           .threePointArc((0, -R), (-R, 0))
           .close())
# Revolve only 180 degrees about the straight edge -> hemisphere
hemi = profile.revolve(180, (0, 0, 0), (1, 0, 0))

# Orient so the flat face is on top (z=0) and the dome points downward
hemi = hemi.rotate((0, 0, 0), (1, 0, 0), -90)

# Cross-shaped groove: two perpendicular 10 mm wide slots, 20 mm deep from the top
box1 = cq.Workplane("XY").box(100, 10, 20).translate((0, 0, -10))
box2 = cq.Workplane("XY").box(10, 100, 20).translate((0, 0, -10))

result = hemi.cut(box1).cut(box2)
