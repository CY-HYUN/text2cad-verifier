import cadquery as cq
import math

# Base shaft: diameter 30, length 80
shaft = cq.Workplane("XY").circle(15).extrude(80)

# Helical path: pitch 20, height 80 (4 turns), on the shaft surface radius
helix = cq.Wire.makeHelix(20, 80, 15)

# Groove profile: circle centred on the surface -> semicircular groove cross-section
profile = cq.Workplane("XZ").center(15, 0).circle(2)

groove = profile.sweep(cq.Workplane(obj=helix), isFrenet=True)

result = shaft.cut(groove)
