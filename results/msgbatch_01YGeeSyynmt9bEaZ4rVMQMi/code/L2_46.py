import cadquery as cq

R = 30.0
offset = 20.0  # vertical offset so the domes overlap and form a waist

# First entity: hemisphere with its flat face toward +Z (dome points down)
sphere1 = cq.Workplane("XY").sphere(R)
cut_box1 = cq.Workplane("XY").box(4 * R, 4 * R, 2 * R, centered=(True, True, False))  # z in [0, 2R]
hemi_up_flat = sphere1.cut(cut_box1)  # keep z <= 0

# Second entity: hemisphere with its flat face toward -Z (dome points up)
sphere2 = cq.Workplane("XY").sphere(R)
cut_box2 = cq.Workplane("XY").box(4 * R, 4 * R, 2 * R, centered=(True, True, False)).translate((0, 0, -2 * R))  # z in [-2R, 0]
hemi_down_flat = sphere2.cut(cut_box2)  # keep z >= 0

# Offset the hemispheres so their domes overlap, creating an "8"-shaped waist
top = hemi_up_flat.translate((0, 0, offset))
bottom = hemi_down_flat.translate((0, 0, -offset))

result = top.union(bottom)
