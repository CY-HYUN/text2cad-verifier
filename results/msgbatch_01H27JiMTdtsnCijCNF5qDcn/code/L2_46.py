import cadquery as cq

R = 30.0

sphere = cq.Workplane("XY").sphere(R)

# Hemisphere 1: flat face toward +Z (dome below, z <= 0)
box_low = cq.Workplane("XY").box(2*R+2, 2*R+2, R+1, centered=(True, True, False)).translate((0, 0, -(R+1)))
hemi1 = sphere.intersect(box_low)

# Hemisphere 2: flat face toward -Z (dome above, z >= 0)
box_up = cq.Workplane("XY").box(2*R+2, 2*R+2, R+1, centered=(True, True, False))
hemi2 = sphere.intersect(box_up)

result = hemi1.union(hemi2)
