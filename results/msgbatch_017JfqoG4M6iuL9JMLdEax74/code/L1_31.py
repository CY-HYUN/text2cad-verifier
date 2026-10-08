import cadquery as cq

result = (
    cq.Workplane("XY")
    .sphere(25)
    .cut(cq.Workplane("XY").box(20, 20, 60))
)
