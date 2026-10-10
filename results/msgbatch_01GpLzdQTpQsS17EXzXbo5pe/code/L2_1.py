import cadquery as cq
import math

# Base cube 50x50x50 centered at origin (extruded 25 both directions in Z)
base = cq.Workplane("XY").rect(50, 50).extrude(25, both=True)

L = 200   # long enough for a through cut
r = 30    # 60 mm diameter
d = 45    # circle centre offset: cuts 10 mm into each side face, leaves the corner edges intact

# Four cylinders running along Z (perpendicular to the XY sketch plane),
# centred in front of / behind / left of / right of the origin
centers = [(d, 0), (-d, 0), (0, d), (0, -d)]
for cx, cy in centers:
    cyl = cq.Solid.makeCylinder(r, L, cq.Vector(cx, cy, -L / 2), cq.Vector(0, 0, 1))
    base = base.cut(cq.Workplane("XY").add(cyl))

result = base
