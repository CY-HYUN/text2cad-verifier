import cadquery as cq

# Frustum: 80x80 base at z=0 lofted to 50x50 top at z=45
frustum = (
    cq.Workplane("XY")
    .rect(80.0, 80.0)
    .workplane(offset=45.0)
    .rect(50.0, 50.0)
    .loft(combine=True)
)

# Blind cavity 30x30, 15 deep from the top face
body = (
    frustum.faces(">Z").workplane()
    .rect(30.0, 30.0)
    .cutBlind(-15.0)
)

# 1.0 mm 45° chamfer on the four cavity-opening edges
result = (
    body.edges(cq.selectors.BoxSelector((-16, -16, 44), (16, 16, 46)))
    .chamfer(1.0)
)
