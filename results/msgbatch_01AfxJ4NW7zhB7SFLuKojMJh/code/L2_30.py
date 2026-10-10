import cadquery as cq

body = cq.Workplane("XY").box(60, 30, 30, centered=(True, True, False))

# semi-cylindrical cut along the long axis (X) on the bottom face
arch = (cq.Workplane("YZ").circle(11).extrude(30, both=True))
body = body.cut(arch)

# vertical holes through the arch
holes = (cq.Workplane("XY").pushPoints([(-15, 0), (15, 0)])
         .circle(3).extrude(30))
body = body.cut(holes)

result = body
