import cadquery as cq

# Main blank: 80 x 60 x 30, centered in XY, bottom at z=0
blank = cq.Workplane("XY").box(80, 60, 30, centered=(True, True, False))

# Notch: 50 x 30 x 20, aligned to +X, +Y, +Z faces (corner at (40,30,30))
notch = (
    cq.Workplane("XY")
    .box(50, 30, 20, centered=False)
    .translate((40 - 50, 30 - 30, 30 - 20))
)

body = blank.cut(notch)

# Fillet the inner (concave) corner edges at the base of the notch
r = 4.0
try:
    result = body.edges(
        cq.selectors.BoxSelector((-10.5, -0.5, 9.5), (40.5, 30.5, 30.5))
    ).edges(
        cq.selectors.BoxSelector((-10.5, -0.5, 9.5), (-9.5, 30.5, 10.5))
    ).fillet(r)
    # also fillet the edge along X at y=0, z=10
    result = result.edges(
        cq.selectors.BoxSelector((-6.5, -0.5, 9.5), (40.5, 0.5, 10.5))
    ).fillet(r)
except Exception:
    try:
        result = body.edges(
            cq.selectors.BoxSelector((-10.5, -0.5, 9.5), (-9.5, 30.5, 10.5))
        ).fillet(r)
    except Exception:
        result = body
