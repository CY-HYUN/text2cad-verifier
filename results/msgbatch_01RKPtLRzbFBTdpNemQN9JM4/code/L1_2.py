import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(20)
    .circle(12.5)
    .extrude(120)
)
