import cadquery as cq

# Cylinder: diameter 20, length 50, axis along Z
cyl = cq.Workplane("XY").circle(10).extrude(50)

# Rectangular cut profile on the front plane (XZ):
# 5 mm wide along the axis, centered at mid-length (z = 25),
# inner edge 1 mm from the axis, outer edge beyond the cylinder surface
cutter = (
    cq.Workplane("XZ")
    .center(6, 25)
    .rect(10, 5)  # x from 1 to 11, z from 22.5 to 27.5
    .revolve(360, (-6, -25, 0), (-6, 1 - 25, 0))  # revolve about the Z axis (x=0)
)

result = cyl.cut(cutter)
