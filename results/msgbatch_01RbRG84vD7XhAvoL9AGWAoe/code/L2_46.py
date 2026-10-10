import cadquery as cq

R = 30.0
offset = 20.0  # lateral misalignment of the two centers

# Left hemisphere: centered at origin, dome toward -X, flat face on X=0
left_sphere = cq.Workplane("XY").sphere(R)
left_keep = cq.Workplane("XY").box(R, 2 * R + 2, 2 * R + 2).translate((-R / 2, 0, 0))
left = left_sphere.intersect(left_keep)

# Right hemisphere: centered at (0, offset, 0), dome toward +X, flat face on X=0
right_sphere = cq.Workplane("XY").sphere(R).translate((0, offset, 0))
right_keep = cq.Workplane("XY").box(R, 2 * R + 2, 2 * R + 2).translate((R / 2, offset, 0))
right = right_sphere.intersect(right_keep)

result = left.union(right)
