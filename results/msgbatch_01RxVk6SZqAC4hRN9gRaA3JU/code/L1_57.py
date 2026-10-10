import cadquery as cq

# Blank: 80 x 60 centered rectangle, extruded 30
L, W, H = 80.0, 60.0, 30.0
blank = cq.Workplane("XY").rect(L, W).extrude(H)

# Notch: 50 (X) x 30 (Y) at the +X/+Y corner, cut 20 deep from top
nx, ny, nd = 50.0, 30.0, 20.0
cx = L / 2 - nx / 2   # 15
cy = W / 2 - ny / 2   # 15
notch = (
    cq.Workplane("XY")
    .workplane(offset=H - nd)
    .center(cx, cy)
    .rect(nx, ny)
    .extrude(nd)
)
body = blank.cut(notch)

# Fillet the inner (concave) vertical corner edge of the notch at (-10, 0)
xi = L / 2 - nx   # -10
yi = W / 2 - ny   # 0
result = (
    body.edges("|Z")
    .edges(cq.selectors.BoxSelector((xi - 0.1, yi - 0.1, H - nd - 0.1),
                                    (xi + 0.1, yi + 0.1, H + 0.1)))
    .fillet(4.0)
)
