import cadquery as cq

# Cylinder: diameter 20, length 50, axis along Z
cyl = cq.Workplane("XY").circle(10).extrude(50)

# Rectangular cut profile in the front (XZ) plane:
# 5 mm wide along the axis, centered at z=25, inner edge at r=1, extending beyond the outer surface
cut_profile = (
    cq.Workplane("XZ")
    .moveTo(1, 22.5)
    .lineTo(11, 22.5)
    .lineTo(11, 27.5)
    .lineTo(1, 27.5)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = cyl.cut(cut_profile)
