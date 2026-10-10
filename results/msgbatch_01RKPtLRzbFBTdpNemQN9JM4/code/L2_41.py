import cadquery as cq
import math

R = 20.0
H = 60.0

# Octagonal prism (circumscribed diameter 40, height 60)
prism = cq.Workplane("XY").polygon(8, 2 * R).extrude(H)

# 45-degree conical cut forming a pointed top: cylinder to z=40, then cone to apex at z=60
profile = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (R + 1, 0), (R + 1, 39), (0, 60)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
body = prism.intersect(profile)

# Horizontal rectangular groove: 5 wide, 2 deep, around the middle
inner_R = R - 2.0 / math.cos(math.radians(22.5))
ring = (
    cq.Workplane("XY")
    .workplane(offset=H / 2 - 2.5)
    .circle(40)
    .extrude(5)
)
core = (
    cq.Workplane("XY")
    .workplane(offset=H / 2 - 2.5)
    .polygon(8, 2 * inner_R)
    .extrude(5)
)
groove = ring.cut(core)

result = body.cut(groove)
