import cadquery as cq

# Base cylinder: diameter 30 mm, height 60 mm, along +Z
cyl = cq.Workplane("XY").circle(15.0).extrude(60.0)

# Lateral through-hole: diameter 10 mm, centered at Z=30, along ±Y
hole = (
    cq.Workplane("XZ")
    .center(0, 30.0)
    .circle(5.0)
    .extrude(50.0, both=True)
)

result = cyl.cut(hole)
