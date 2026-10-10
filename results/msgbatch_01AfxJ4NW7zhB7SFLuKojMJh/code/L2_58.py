import cadquery as cq

box = cq.Workplane("XY").box(80, 40, 40, centered=False)

d = 10  # hole diameter (not specified; chosen)

# Horizontal hole from the left face (x=0), center at y=20, z=20, 40 mm deep
h_hole = (cq.Workplane("YZ").center(20, 20).circle(d / 2).extrude(40))

# Vertical hole from top face (z=40), center at x=40, y=20, 20 mm deep
v_hole = (cq.Workplane("XY").workplane(offset=40).center(40, 20)
          .circle(d / 2).extrude(-20))

result = box.cut(h_hole).cut(v_hole)
