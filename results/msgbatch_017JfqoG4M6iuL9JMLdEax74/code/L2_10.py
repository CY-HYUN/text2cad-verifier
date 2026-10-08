import cadquery as cq

# Base plate: 80 (X) x 40 (Y) x 10 (Z)
base = cq.Workplane("XY").box(80, 40, 10).translate((0, 0, 5))

# Flanges: 10 thick (X), 40 wide (Y), 40 high (Z) on top of base at both ends
left = cq.Workplane("XY").box(10, 40, 40).translate((-35, 0, 30))
right = cq.Workplane("XY").box(10, 40, 40).translate((35, 0, 30))

body = base.union(left).union(right)

# Through holes (dia 10) at flange centers, along X
hole = (cq.Workplane("YZ").workplane(offset=-50)
        .center(0, 30).circle(5).extrude(100))
body = body.cut(hole)

# Counterbore (dia 20, 2 deep) on outer face of right flange
cb = (cq.Workplane("YZ").workplane(offset=38)
      .center(0, 30).circle(10).extrude(5))
body = body.cut(cb)

result = body
