import cadquery as cq

outer = (
    cq.Workplane("XY")
    .circle(40)
    .circle(30)
    .extrude(20)
)

inner = (
    cq.Workplane("XY")
    .circle(20)
    .circle(10)
    .extrude(20)
)

result = outer.union(inner)
