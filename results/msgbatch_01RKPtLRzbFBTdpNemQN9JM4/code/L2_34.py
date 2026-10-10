import cadquery as cq

# Base cylinder: diameter 20, length 50, axis along Z
base = cq.Workplane("XY").circle(10).extrude(50)

# Circumferential groove: 5 wide, 9 deep (remaining core radius 1 -> diameter 2)
outer_r = 11  # exceed the cylinder radius to ensure a clean cut
inner_r = 10 - 9
ring = (
    cq.Workplane("XY")
    .workplane(offset=25 - 2.5)
    .circle(outer_r)
    .circle(inner_r)
    .extrude(5)
)

result = base.cut(ring)
