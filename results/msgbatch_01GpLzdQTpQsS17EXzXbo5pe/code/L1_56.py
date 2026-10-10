import cadquery as cq

# Frustum: 80x80 base lofted to 50x50 top at height 45
result = (
    cq.Workplane("XY")
    .rect(80, 80)
    .workplane(offset=45)
    .rect(50, 50)
    .loft(combine=True)
)

# 30x30 blind cavity, 15 deep from the top face
result = (
    result.faces(">Z").workplane()
    .rect(30, 30)
    .cutBlind(-15)
)

# Chamfer the four cavity-opening edges (at z=45, within |x|,|y| <= 15)
result = (
    result.edges(cq.selectors.BoxSelector((-16, -16, 44), (16, 16, 46)))
    .chamfer(1.0)
)
