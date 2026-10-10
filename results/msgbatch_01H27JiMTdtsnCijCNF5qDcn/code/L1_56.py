import cadquery as cq

# Frustum: loft from 80x80 square at z=0 to 50x50 square at z=45
frustum = (
    cq.Workplane("XY")
    .rect(80.0, 80.0)
    .workplane(offset=45.0)
    .rect(50.0, 50.0)
    .loft(combine=True)
)

# Blind cavity 30x30, 15 deep from top face
cavity = (
    cq.Workplane("XY")
    .workplane(offset=45.0 - 15.0)
    .rect(30.0, 30.0)
    .extrude(15.0)
)
body = frustum.cut(cavity)

# Chamfer the four edges of the cavity opening (on top face, the inner square edges)
result = (
    body.faces(">Z")
    .edges(cq.selectors.BoxSelector((-16, -16, 44), (16, 16, 46)))
    .chamfer(1.0)
)
