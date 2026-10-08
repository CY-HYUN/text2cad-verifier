import cadquery as cq

R = 30.0
offset = 25.0  # offset so the domes overlap slightly, forming a waist

# Hemisphere with flat face toward +Z (dome pointing down)
sphere1 = cq.Workplane("XY").sphere(R)
cut1 = cq.Workplane("XY").box(2 * R + 2, 2 * R + 2, R + 1, centered=(True, True, False)).translate((0, 0, -R - 1))
hemi_up_flat = sphere1.intersect(cut1).translate((0, 0, offset))

# Hemisphere with flat face toward -Z (dome pointing up)
sphere2 = cq.Workplane("XY").sphere(R)
cut2 = cq.Workplane("XY").box(2 * R + 2, 2 * R + 2, R + 1, centered=(True, True, False))
hemi_down_flat = sphere2.intersect(cut2).translate((0, 0, -offset))

# Union to form an "8"-shaped waist
result = hemi_up_flat.union(hemi_down_flat)
