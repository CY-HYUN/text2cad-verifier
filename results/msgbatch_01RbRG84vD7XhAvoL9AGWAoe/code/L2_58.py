import cadquery as cq

L, W, H = 80.0, 40.0, 40.0
d = 10.0
r = d / 2.0

body = cq.Workplane("XY").box(L, W, H)

# Horizontal bore from the centre of the left face (x = -40), 40 mm deep
h_hole = (
    cq.Workplane("YZ")
    .workplane(offset=-L / 2)
    .circle(r)
    .extrude(40.0)
)

# Vertical bore from the centre of the top face (z = +20), 20 mm deep
v_hole = (
    cq.Workplane("XY")
    .workplane(offset=H / 2)
    .circle(r)
    .extrude(-20.0)
)

# Small sphere at the junction for a clean bend
joint = cq.Workplane("XY").sphere(r)

result = body.cut(h_hole).cut(v_hole).cut(joint)
