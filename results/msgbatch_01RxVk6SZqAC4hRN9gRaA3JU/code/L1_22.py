import cadquery as cq

# Square frustum: 60 mm square base lofted to 40 mm square top over 30 mm height
frustum = (
    cq.Workplane("XY")
    .rect(60.0, 60.0)
    .workplane(offset=30.0)
    .rect(40.0, 40.0)
    .loft(combine=True)
)

# Central 20 mm diameter hole cut through the full height
hole = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .circle(10.0)
    .extrude(32.0)
)

result = frustum.cut(hole)
