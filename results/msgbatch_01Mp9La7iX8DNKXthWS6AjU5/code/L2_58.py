import cadquery as cq

d = 10.0  # hole diameter

block = cq.Workplane("XY").box(80, 40, 40, centered=(True, True, False))

# Left-face hole: from x=-40 face, centered at z=20, 40 mm deep along +X (ends at x=0)
left_hole = (
    cq.Workplane("YZ", origin=(-40, 0, 0))
    .center(0, 20)
    .circle(d / 2)
    .extrude(40)
)

# Top-face hole: centered on top, 20 mm deep (z=40 down to z=20)
top_hole = (
    cq.Workplane("XY", origin=(0, 0, 20))
    .circle(d / 2)
    .extrude(20)
)

result = block.cut(left_hole).cut(top_hole)
