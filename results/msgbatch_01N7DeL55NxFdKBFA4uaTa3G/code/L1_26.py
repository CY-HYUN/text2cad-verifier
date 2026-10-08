import cadquery as cq

R = 30.0
cut_z = 15.0

sphere = cq.Workplane("XY").sphere(R)
# Keep portion below z = 15
box = cq.Workplane("XY").box(4 * R, 4 * R, 4 * R).translate((0, 0, cut_z - 2 * R))
result = sphere.intersect(box)
