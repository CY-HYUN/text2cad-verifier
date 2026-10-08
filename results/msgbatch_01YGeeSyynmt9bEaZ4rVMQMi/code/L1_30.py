import cadquery as cq

# Cylinder: diameter 30 mm, height 60 mm along +Z
cyl = cq.Workplane("XY").circle(15.0).extrude(60.0)

# Lateral through-hole: diameter 10 mm on XZ plane at (x=0, z=30), cut along ±Y
hole = (
    cq.Workplane("XZ")
    .center(0, 30.0)
    .circle(5.0)
    .extrude(50.0, both=True)
)

result = cyl.cut(hole)
