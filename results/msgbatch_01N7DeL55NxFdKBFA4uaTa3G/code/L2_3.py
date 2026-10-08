import cadquery as cq

R = 40.0
slot_w = 10.0
slot_depth = 20.0
slot_len = 2 * R + 20.0  # extends beyond the hemisphere edge

# Hemisphere: flat face on top (z=0), dome below
sphere = cq.Workplane("XY").sphere(R)
lower_box = cq.Workplane("XY").box(3 * R, 3 * R, R, centered=(True, True, False)).translate((0, 0, -R))
hemi = sphere.intersect(lower_box)

# Cross-shaped slot cut downward from the top face
slot1 = cq.Workplane("XY").box(slot_len, slot_w, slot_depth).translate((0, 0, -slot_depth / 2))
slot2 = cq.Workplane("XY").box(slot_w, slot_len, slot_depth).translate((0, 0, -slot_depth / 2))

result = hemi.cut(slot1).cut(slot2)
