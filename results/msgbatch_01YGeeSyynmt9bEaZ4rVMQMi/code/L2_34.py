import cadquery as cq

# Main cylinder: diameter 20 mm, length 50 mm, axis along Z, centered at origin
cyl = cq.Workplane("XY").circle(10).extrude(50).translate((0, 0, -25))

# Rectangle sketch on the front view plane (XZ): 5 mm wide (along axis), centered,
# inner edge 1 mm from the axis, extending past the outer surface
cutter = (
    cq.Workplane("XZ")
    .moveTo(1, -2.5)
    .lineTo(11, -2.5)
    .lineTo(11, 2.5)
    .lineTo(1, 2.5)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))  # revolve about the cylinder axis (Z)
)

result = cyl.cut(cutter)
