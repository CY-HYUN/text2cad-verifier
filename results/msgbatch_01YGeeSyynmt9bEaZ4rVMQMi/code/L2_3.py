import cadquery as cq

R = 40.0
# Hemisphere with flat face on top (z=0), dome below
sphere = cq.Workplane("XY").sphere(R)
box = cq.Workplane("XY").box(2 * R + 10, 2 * R + 10, R + 5, centered=(True, True, False)).translate((0, 0, -(R + 5)))
hemi = sphere.intersect(box)

# Cross-shaped groove: two perpendicular 10mm-wide slots, 20mm deep from top
L = 2 * R + 20
slot1 = cq.Workplane("XY").box(L, 10, 20, centered=(True, True, False)).translate((0, 0, -20))
slot2 = cq.Workplane("XY").box(10, L, 20, centered=(True, True, False)).translate((0, 0, -20))

result = hemi.cut(slot1).cut(slot2)
