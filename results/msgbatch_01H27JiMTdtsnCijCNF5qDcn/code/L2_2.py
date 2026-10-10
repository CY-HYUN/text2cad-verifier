import cadquery as cq

sphere = cq.Workplane("XY").sphere(40)

cutter = (
    cq.Workplane("XY")
    .workplane(offset=-50)
    .center(25, 0)
    .circle(15)
    .extrude(100)
)

result = sphere.cut(cutter)
