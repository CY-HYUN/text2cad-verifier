import cadquery as cq

L, W, H = 80.0, 40.0, 40.0
d = 10.0  # hole diameter (same for both holes)

# Base block centered at origin
body = cq.Workplane("XY").box(L, W, H)

# Side hole: from left face (x=-40) toward +X, depth 40 -> ends at x=0 (center)
side_hole = (
    cq.Workplane("YZ", origin=(-L / 2, 0, 0))
    .circle(d / 2)
    .extrude(40.0)
)

# Top hole: from top face center (z=+20) downward, depth 20 -> ends at z=0 (side hole axis)
top_hole = (
    cq.Workplane("XY", origin=(0, 0, H / 2))
    .circle(d / 2)
    .extrude(-20.0)
)

result = body.cut(side_hole).cut(top_hole)
