import cadquery as cq

# T-shaped profile: top bar 100 x 20, stem 20 wide extending 60 down
pts = [
    (-50, 10), (50, 10), (50, -10), (10, -10),
    (10, -70), (-10, -70), (-10, -10), (-50, -10),
]
block = cq.Workplane("XY").polyline(pts).close().extrude(20)

# Fillet all edges
try:
    block = block.edges().fillet(8)
except Exception:
    try:
        block = block.edges().fillet(7.5)
    except Exception:
        pass

# Through holes (5 mm diameter) at the centres of the three flat ends
hole_x = (
    cq.Workplane("YZ")
    .workplane(offset=-60)
    .center(0, 10)
    .circle(2.5)
    .extrude(120)
)
hole_y = (
    cq.Workplane("XZ")
    .workplane(offset=-20)
    .center(0, 10)
    .circle(2.5)
    .extrude(100)
)

result = block.cut(hole_x).cut(hole_y)
