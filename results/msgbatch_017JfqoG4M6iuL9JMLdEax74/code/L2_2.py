import cadquery as cq

sphere = cq.Workplane("XY").sphere(40)
cyl = (
    cq.Workplane("XY")
    .workplane(offset=-60)
    .center(25, 0)
    .circle(15)
    .extrude(120)
)
result = sphere.cut(cyl)
