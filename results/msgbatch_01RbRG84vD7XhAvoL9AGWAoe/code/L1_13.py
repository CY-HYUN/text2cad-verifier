import cadquery as cq

# Horizontal cylinder along X: diameter 20, length 80, axis at z=40
horiz = (
    cq.Workplane("YZ")
    .workplane(offset=-40)
    .center(0, 40)
    .circle(10)
    .extrude(80)
)

# Vertical cylinder along Z: diameter 20, length 40, meeting horizontal axis at midpoint
vert = cq.Workplane("XY").circle(10).extrude(40)

result = horiz.union(vert)
