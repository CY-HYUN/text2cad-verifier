import cadquery as cq

cube = cq.Workplane("XY").box(50, 50, 50)

# Blind hole along X from the -X face, 30 deep, centred at y=0, z=0
hole_x = (cq.Workplane("YZ").workplane(offset=-25)
          .circle(7.5).extrude(30))

# Blind hole along Z from the +Z face, 30 deep, centred at x=0, y=0
hole_z = (cq.Workplane("XY").workplane(offset=25)
          .circle(7.5).extrude(-30))

result = cube.cut(hole_x).cut(hole_z)
