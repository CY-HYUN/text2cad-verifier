import cadquery as cq

base = cq.Workplane("XY").box(60, 60, 10, centered=(True, True, False))
cyl = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .circle(15)
    .extrude(50)
)
result = base.union(cyl)
