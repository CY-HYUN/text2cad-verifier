import cadquery as cq

# Solid cylinder: D60, H80, base at origin, axis along Z
cyl = cq.Workplane("XY").circle(30).extrude(80)

# External groove from Z=35 to Z=45, groove bottom diameter 54
ring = (
    cq.Workplane("XY")
    .workplane(offset=35)
    .circle(31)
    .circle(27)
    .extrude(10)
)
body = cyl.cut(ring)

# Round the outer edges on both sides of the groove (R1)
try:
    body = body.edges(
        cq.selectors.BoxSelector((-31, -31, 34.9), (31, 31, 45.1))
    ).edges(
        cq.selectors.RadiusNthSelector(1)
    ).fillet(1.0)
except Exception:
    try:
        sel = cq.selectors.BoxSelector((-31, -31, 34.9), (31, 31, 45.1))
        body = body.edges(sel).fillet(1.0)
    except Exception:
        pass

result = body
