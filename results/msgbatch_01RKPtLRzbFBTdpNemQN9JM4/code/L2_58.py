import cadquery as cq

L, W, H = 80.0, 40.0, 40.0
d = 10.0  # hole diameter (not specified in the description)

body = cq.Workplane("XY").box(L, W, H, centered=False)

# Horizontal segment: from the left face (x=0) centre, 40 mm deep along +x
h_hole = (
    cq.Workplane("YZ")
    .center(W / 2, H / 2)
    .circle(d / 2)
    .extrude(40)
)

# Vertical segment: from the top face centre (x=40, y=20), 20 mm deep down to z=20
v_hole = (
    cq.Workplane("XY", origin=(0, 0, H))
    .center(40, W / 2)
    .circle(d / 2)
    .extrude(-20)
)

result = body.cut(h_hole).cut(v_hole)
