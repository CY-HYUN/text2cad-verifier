import cadquery as cq
import math

R = 40.0
groove_w = 10.0
groove_depth = 25.0

# Hemisphere with flat face at z=0, dome above
sphere = cq.Workplane("XY").sphere(R)
half_box = cq.Workplane("XY").box(2*R+10, 2*R+10, R+5, centered=(True, True, False))
hemi = sphere.intersect(half_box)

# Cross-shaped groove cut from the flat face, open at the curved boundary
L = 2*R + 20
bar1 = cq.Workplane("XY").box(L, groove_w, groove_depth, centered=(True, True, False))
bar2 = cq.Workplane("XY").box(groove_w, L, groove_depth, centered=(True, True, False))
cross = bar1.union(bar2)

result = hemi.cut(cross)
