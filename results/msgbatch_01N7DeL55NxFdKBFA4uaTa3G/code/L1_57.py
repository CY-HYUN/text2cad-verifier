import cadquery as cq

# Blank: 80 x 60 centered rectangle, extruded 30
blank = cq.Workplane("XY").rect(80.0, 60.0).extrude(30.0)

# Notch: 50 (X) x 30 (Y) at the +X/+Y corner, cut 20 deep from top
nx, ny, depth = 50.0, 30.0, 20.0
x0, x1 = 40.0 - nx, 40.0
y0, y1 = 30.0 - ny, 30.0
notch = (
    cq.Workplane("XY")
    .workplane(offset=30.0 - depth)
    .center((x0 + x1) / 2, (y0 + y1) / 2)
    .rect(nx, ny)
    .extrude(depth)
)
body = blank.cut(notch)

# Fillet the inner (concave) corner edges of the notch
zf = 30.0 - depth
try:
    result = (
        body.edges(
            cq.selectors.BoxSelector((x0 - 0.1, y0 - 0.1, zf - 0.1), (x1 - 0.1, y1 - 0.1, 30.0 - 0.1))
        )
        .fillet(4.0)
    )
    if not result.val().isValid():
        raise ValueError
except Exception:
    # Fallback: fillet only the vertical inner corner edge
    result = (
        body.edges("|Z")
        .edges(cq.selectors.BoxSelector((x0 - 0.1, y0 - 0.1, zf - 0.1), (x0 + 0.1, y0 + 0.1, 30.1)))
        .fillet(4.0)
    )
