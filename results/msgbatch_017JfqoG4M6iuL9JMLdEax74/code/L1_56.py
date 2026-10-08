import cadquery as cq

bottom = cq.Workplane("XY").rect(80, 80)
frustum = (
    cq.Workplane("XY")
    .rect(80, 80)
    .workplane(offset=45)
    .rect(50, 50)
    .loft(combine=True)
)

cavity = (
    cq.Workplane("XY")
    .workplane(offset=45 - 15)
    .rect(30, 30)
    .extrude(15)
)

body = frustum.cut(cavity)

# Chamfer the four edges of the cavity opening at the top surface
try:
    body = (
        body.edges(cq.selectors.BoxSelector((-16, -16, 44.9), (16, 16, 45.1)))
        .chamfer(1.0)
    )
except Exception:
    pass

result = body
