import cadquery as cq

L, W, H = 80.0, 40.0, 40.0
D = 10.0  # hole diameter (shared by both holes)

# Main block centred at origin: X[-40,40], Y[-20,20], Z[-20,20]
block = cq.Workplane("XY").box(L, W, H)

# Side hole: from left face (x=-40) at face centre, 40 mm deep along +X -> ends at x=0
side_hole = (
    cq.Workplane("YZ", origin=(-L / 2, 0, 0))
    .circle(D / 2)
    .extrude(40.0)
)

# Top hole: from top face centre (z=20), 20 mm deep along -Z -> ends at z=0
top_hole = (
    cq.Workplane("XY", origin=(0, 0, H / 2))
    .circle(D / 2)
    .extrude(-20.0)
)

# Both holes meet at the block centre, forming an L-shaped internal channel
result = block.cut(side_hole).cut(top_hole)
