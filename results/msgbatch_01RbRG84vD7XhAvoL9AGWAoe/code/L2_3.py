import cadquery as cq

R = 40.0
groove_w = 10.0
groove_d = 25.0

# Hemisphere with flat face on top (z = 0), dome below
sphere = cq.Workplane("XY").sphere(R)
keep = cq.Workplane("XY").box(3 * R, 3 * R, R, centered=(True, True, False)).translate((0, 0, -R))
hemi = sphere.intersect(keep)

# Cross-shaped groove cut from the flat face, open at the curved boundary
L = 2.5 * R
g1 = cq.Workplane("XY").box(L, groove_w, groove_d).translate((0, 0, -groove_d / 2))
g2 = cq.Workplane("XY").box(groove_w, L, groove_d).translate((0, 0, -groove_d / 2))
cross = g1.union(g2)

result = hemi.cut(cross)
