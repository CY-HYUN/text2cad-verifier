import cadquery as cq
import math

R = 40.0
w = 10.0
depth = 25.0
L = 100.0

# Hemisphere: dome pointing down, flat face at z=0
sphere = cq.Workplane("XY").sphere(R)
lower_box = cq.Workplane("XY").box(2*R+10, 2*R+10, R+5, centered=(True, True, False)).translate((0, 0, -(R+5)))
hemi = sphere.intersect(lower_box)

# Cross-shaped groove cutter, from z=0 down to z=-depth (extended slightly above)
bar1 = cq.Workplane("XY").box(L, w, depth+5, centered=(True, True, False)).translate((0, 0, -depth))
bar2 = cq.Workplane("XY").box(w, L, depth+5, centered=(True, True, False)).translate((0, 0, -depth))
cross = bar1.union(bar2)

result = hemi.cut(cross)
