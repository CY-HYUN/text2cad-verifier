import cadquery as cq

# Frustum: bottom 80x80, top 50x50, height 45
base = (
    cq.Workplane("XY")
    .rect(80, 80)
    .workplane(offset=45)
    .rect(50, 50)
    .loft(combine=True)
)

# Square blind cavity 30x30, depth 15 from top face
cavity = (
    cq.Workplane("XY")
    .workplane(offset=30)
    .rect(30, 30)
    .extrude(15)
)

body = base.cut(cavity)

# Chamfer the top opening edges of the cavity (1 mm)
result = (
    body.faces(">Z")
    .edges(cq.selectors.BoxSelector((-16, -16, 44), (16, 16, 46)))
    .chamfer(1)
)
