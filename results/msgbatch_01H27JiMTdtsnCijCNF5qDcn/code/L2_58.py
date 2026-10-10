import cadquery as cq

d = 10.0
block = cq.Workplane("XY").box(80, 40, 40, centered=False)

# Horizontal hole from left face (X=0), center at Y=20,Z=20, depth 40 along +X
h1 = (cq.Workplane("YZ").workplane(offset=0)
      .center(20, 20).circle(d/2).extrude(40))

# Vertical hole from top face (Z=40) at X=40,Y=20, depth 20 downward
h2 = (cq.Workplane("XY").workplane(offset=40)
      .center(40, 20).circle(d/2).extrude(-20))

result = block.cut(h1).cut(h2)
