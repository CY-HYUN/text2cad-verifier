import cadquery as cq
import math

# Octagon: circumscribed diameter 40 mm, extruded 60 mm
R = 20.0
H = 60.0
body = cq.Workplane("XY").polygon(8, 2 * R).extrude(H)

# Sharpen the top: 45-degree triangle in the front (XZ) plane,
# revolved about the central Z axis
ext = R + 2.0  # extend past the corners for a clean cut
tip_cut = (
    cq.Workplane("XZ")
    .polyline([(0, H), (ext, H), (ext, H - ext)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
body = body.cut(tip_cut)

# Annular groove at mid-height: 5 mm wide, 2 mm deep from the edge
groove_w = 5.0
groove_r = R - 2.0
zc = H / 2.0
groove = (
    cq.Workplane("XZ")
    .polyline([
        (groove_r, zc - groove_w / 2),
        (ext, zc - groove_w / 2),
        (ext, zc + groove_w / 2),
        (groove_r, zc + groove_w / 2),
    ])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
body = body.cut(groove)

result = body
