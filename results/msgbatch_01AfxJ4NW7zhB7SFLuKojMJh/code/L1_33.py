import cadquery as cq

L = 100.0
R_out = 30.0
R_in = 20.0

# Cylinders with axis along X (profile drawn in the YZ plane, extruded along +X)
outer = cq.Workplane("YZ").circle(R_out).extrude(L)
inner = cq.Workplane("YZ").circle(R_in).extrude(L)

# Keep only the half with Z >= 0
keep = cq.Workplane("XY").box(L, 2 * R_out, R_out, centered=False).translate((0, -R_out, 0))

result = outer.cut(inner).intersect(keep)
