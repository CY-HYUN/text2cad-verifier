import cadquery as cq

L, W, H = 100.0, 40.0, 30.0

# Base rectangular prism (X = length, Y = width, Z = height)
body = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Semicircular channel: R15 centered on the upper edge of the end face, through full length
channel = (
    cq.Workplane("YZ")
    .workplane(offset=-L / 2 - 1)
    .center(0, H)
    .circle(15.0)
    .extrude(L + 2)
)
body = body.cut(channel)

# Side groove: 60 x 10 rectangle centered on the side face, cut 5 mm deep
groove_depth = 5.0
groove = (
    cq.Workplane("XY")
    .box(60.0, groove_depth, 10.0)
    .translate((0, W / 2 - groove_depth / 2, H / 2))
)
# Mirror the groove to the opposite side
groove_mirror = groove.mirror("XZ")

body = body.cut(groove).cut(groove_mirror)

result = body
