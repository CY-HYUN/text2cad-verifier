import cadquery as cq

R = 30.0
offset = 20.0  # lateral misalignment of the two hemisphere centers

# Left hemisphere: center at origin, dome toward -X, flat face on plane X=0
left_sphere = cq.Workplane("XY").sphere(R)
left_keep = cq.Workplane("XY").box(R, 2 * R + 2, 2 * R + 2).translate((-R / 2, 0, 0))
left_hemi = left_sphere.intersect(left_keep)

# Right hemisphere: center offset in Y, dome toward +X, flat face on plane X=0
right_sphere = cq.Workplane("XY").sphere(R).translate((0, offset, 0))
right_keep = cq.Workplane("XY").box(R, 2 * R + 2, 2 * R + 2).translate((R / 2, offset, 0))
right_hemi = right_sphere.intersect(right_keep)

# Fuse: flat faces coincide (distance 0) but are misaligned
result = left_hemi.union(right_hemi)
