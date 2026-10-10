import cadquery as cq

# Main block: 60 x 40 x 40 mm, base on z = 0
L, W, H = 60.0, 40.0, 40.0
d = 10.0          # channel diameter
spacing = 30.0    # hole center distance
x1, x2 = -spacing / 2, spacing / 2
z_ch = 10.0       # height of the horizontal channel axis

block = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Two vertical holes drilled down from the top face to the channel level
vertical = (
    cq.Workplane("XY")
    .workplane(offset=z_ch)
    .pushPoints([(x1, 0), (x2, 0)])
    .circle(d / 2)
    .extrude(H - z_ch + 1)
)

# Ball joints at the bottom of each hole for a smooth bend
balls = (
    cq.Workplane("XY")
    .pushPoints([(x1, 0, z_ch), (x2, 0, z_ch)])
    .sphere(d / 2)
)

# Internal horizontal channel linking the two holes (hidden inside the block)
lateral = (
    cq.Workplane("YZ")
    .workplane(offset=x1)
    .center(0, z_ch)
    .circle(d / 2)
    .extrude(spacing)
)

channel = vertical.union(balls).union(lateral)

# Remove the U-shaped channel from the block
result = block.cut(channel)
