import cadquery as cq

# Frustum: loft from 80x80 bottom square to 50x50 top square, height 45
frustum = (
    cq.Workplane("XY")
    .rect(80.0, 80.0)
    .workplane(offset=45.0)
    .rect(50.0, 50.0)
    .loft(combine=True)
)

# Blind cavity 30x30, 15 deep from the top surface
cavity = (
    cq.Workplane("XY")
    .workplane(offset=45.0 - 15.0)
    .rect(30.0, 30.0)
    .extrude(15.0)
)
body = frustum.cut(cavity)

# 1.0 mm 45° chamfer on the four cavity opening edges
result = body.edges(
    cq.selectors.BoxSelector((-16.0, -16.0, 44.5), (16.0, 16.0, 45.5))
).chamfer(1.0)
