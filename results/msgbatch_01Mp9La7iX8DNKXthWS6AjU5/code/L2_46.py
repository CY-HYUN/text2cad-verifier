import cadquery as cq

R = 30.0

# Full sphere used as the base for both hemispheres
sphere = cq.Workplane("XY").sphere(R)

# Hemisphere 1: flat face toward +Z (dome extends into -Z)
keep_lower = cq.Workplane("XY").box(2*R + 2, 2*R + 2, R + 1, centered=(True, True, False)).translate((0, 0, -(R + 1)))
hemi1 = sphere.intersect(keep_lower)

# Hemisphere 2: flat face toward -Z (dome extends into +Z)
keep_upper = cq.Workplane("XY").box(2*R + 2, 2*R + 2, R + 1, centered=(True, True, False))
hemi2 = sphere.intersect(keep_upper)

# Boolean union of the two hemispheres
result = hemi1.union(hemi2)
