import cadquery as cq

# Cylinder: diameter 20 mm, length 50 mm, axis along Z
D = 20.0
L = 50.0
cyl = cq.Workplane("XY").circle(D / 2).extrude(L)

# Rectangular cut profile in the front (XZ) plane, centered along the length
groove_w = 5.0
r_inner = 1.0                   # inner edge 1 mm from the axis -> 2 mm diameter neck
r_outer = D / 2 + 1.0           # extend past the outer surface for a clean cut
z0 = L / 2 - groove_w / 2

cutter = (
    cq.Workplane("XZ")
    .moveTo(r_inner, z0)
    .lineTo(r_outer, z0)
    .lineTo(r_outer, z0 + groove_w)
    .lineTo(r_inner, z0 + groove_w)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))  # revolve about the cylinder axis (Z)
)

result = cyl.cut(cutter)
