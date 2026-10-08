import cadquery as cq

# Blank: 80 x 60 centered rectangle, extruded 30
blank = cq.Workplane("XY").rect(80.0, 60.0).extrude(30.0)

# Notch: 50 (X) x 30 (Y) at the +X/+Y corner, cut 20 deep from top
nx, ny, depth = 50.0, 30.0, 20.0
cx = 40.0 - nx / 2.0
cy = 30.0 - ny / 2.0
cutter = (
    cq.Workplane("XY")
    .workplane(offset=30.0 - depth)
    .center(cx, cy)
    .rect(nx, ny)
    .extrude(depth)
)
part = blank.cut(cutter)

# Fillet the inner (concave) corner edges of the notch
x0, y0, zf = 40.0 - nx, 30.0 - ny, 30.0 - depth
try:
    result = part.edges(
        cq.selectors.BoxSelector((x0 - 0.1, y0 - 0.1, zf - 0.1), (x0 + 0.1, y0 + 0.1, 30.1))
    ).fillet(4.0)
except Exception:
    result = part
