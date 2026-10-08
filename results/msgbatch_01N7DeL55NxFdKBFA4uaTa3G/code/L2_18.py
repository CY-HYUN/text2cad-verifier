import cadquery as cq

L, W, H = 100.0, 40.0, 30.0
R = 15.0
gL, gH, gD = 60.0, 10.0, 5.0

# Base prism, centered at origin (z from -15 to 15)
body = cq.Workplane("XY").box(L, W, H)

# Semicircular channel along the full length, centered on top edge of end face
channel = (
    cq.Workplane("YZ")
    .workplane(offset=-L / 2 - 1)
    .center(0, H / 2)
    .circle(R)
    .extrude(L + 2)
)
body = body.cut(channel)

# Side groove on +Y face: 60x10 rectangle, centered, 5 mm deep
groove = cq.Workplane("XY").box(gL, gD, gH).translate((0, W / 2 - gD / 2, 0))
# Mirror to the other side
groove_mirror = groove.mirror("XZ")

body = body.cut(groove).cut(groove_mirror)

result = body
