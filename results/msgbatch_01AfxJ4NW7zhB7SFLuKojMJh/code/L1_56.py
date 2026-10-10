import cadquery as cq

# Frustum via loft from 80x80 at z=0 to 50x50 at z=45
base = (
    cq.Workplane("XY")
    .rect(80, 80)
    .workplane(offset=45)
    .rect(50, 50)
    .loft(combine=True)
)

# Square blind cavity 30x30, depth 15 from top
cavity = (
    cq.Workplane("XY")
    .workplane(offset=30)
    .rect(30, 30)
    .extrude(15)
)
body = base.cut(cavity)

# Chamfer the four edges of the cavity opening at top face (z=45)
result = (
    body.faces(">Z")
    .edges(cq.selectors.BoxSelector((-16, -16, 44), (16, 16, 46)))
    .chamfer(1)
)
